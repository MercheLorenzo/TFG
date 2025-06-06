"""
app.py - Servidor principal de la API SANTRA™ Core Template

Este archivo define la aplicación FastAPI que implementa el backend para los microservicios del template SANTRA™. 
Proporciona funcionalidades como manejo de rutas, conexión a la base de datos, soporte para múltiples idiomas, 
y documentación interactiva de la API.

### Características principales:
- **Rutas principales**: Define rutas para obtener usuarios, realizar cálculos, obtener el tiempo y más.
- **Conexión a MongoDB**: Conexión asíncrona a la base de datos MongoDB mediante motor.
- **Internacionalización**: Soporte para cargar diccionarios de idiomas desde parámetros de la URL.
- **Middleware**: Incluye middlewares para registro de logs, manejo de excepciones y compresión de respuestas.
- **Documentación de la API**: Generación de documentación interactiva usando Swagger y ReDoc.
- **SSL y configuración del entorno**: Soporte para carga de configuraciones según el entorno (producción/desarrollo) y conexión segura en producción.
- **Manejo de errores**: Captura de errores globales y respuestas detalladas.

Este archivo es el punto de entrada para iniciar el servidor FastAPI. El entorno de ejecución y las configuraciones específicas se manejan desde archivos `.env`.

Ejecuta la aplicación con el siguiente comando:
    python src/app.py
O con este comando para producción:
    ENV_FILE=.env.production python src/app.py

Asegúrate de tener las dependencias necesarias instaladas y de que la base de datos esté configurada correctamente antes de iniciar la aplicación.
"""
import sys
import logging
import colorlog
import time
import threading
import ssl
import os
import datetime
import uvicorn
import asyncio
from dotenv import load_dotenv, dotenv_values
from src.Config.config import config #importante cargarlo al principio
# Despues FastAPI
from fastapi import FastAPI, Request, Response, Depends
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel
from src.Content.i18n import load_dictionary, get_current_language
from pymongo import MongoClient
from src.Content.i18n import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE
# Para que la app FastAPI devuelva el contenido de main.html en lugar de solo un mensaje JSON, usamos FileResponse de fastapi.responses para servir archivos HTML
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.Routes.mainRoutes import mainRouter as api_mainRouter
from src.Routes.sampleRoutes import sampleRouter as api_sampleRouter
from src.Routes.userRoutes import userRouter as api_userRouter
from src.Routes.azureRoutes import azureRouter as api_azureRouter
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from http import HTTPStatus  # Para obtener los mensajes de los códigos de estado
from src.Lib.helpers.nomia_utils import debug_log
from contextlib import asynccontextmanager
from src.Routes.workerRoutes import workerRouter as api_workerRouter
from src.Controllers.workerController import check_database_connection_workers
from src.Controllers.userController import check_database_connection_users
# from azure.ai.translation.text import TextTranslationClient
# from azure.core.credentials import AzureKeyCredential
from contextlib import asynccontextmanager

# Descripcion que se muestra en la documentacion de fastapi, en /docs
description = """
santra-core-template

Backend template for santra microservices

## Technical Reference: API _SANTRA™ CORE TEMPLATE_ - FastAPI

![Nomia Energy](static/santraPeque.jpg)

----
Online Interactive API documentation to test all the functions included in _SANTRA™ Core Template_ API.

**¡Warning!**
Don't use the api functions if you are not confortable with the application. It could originate information losses.

----

## Users - DB

You will be able to:

* **Create user** 
* **Get user by email**
* **Count users**
* **Search user by name or last name**

## Workers - DB

You will be able to:

* **Create worker** 
* **Get worker by email**
* **Count workers**
* **Search worker by name or last name**

## Other routes

You can also:

* **Sum two numbers**
* **Get current time UTC**
* **Get current time CET**
* **Generate random string**
* **Get boiler/room weather info** (simulated)
* **Get server status** (main route)
* **Get API version** (main route)
* **Generate token**
* **Verify token**
* **Get error sample** (main route)

----

### Contact Info

For more information, visit [Nomia Energy](https://www.nomiaenergy.com) or contact support at [support@nomiaenergy.com](mailto:support@nomiaenergy.com).

Santra Core Template by Nomia Energy - [http://www.nomiaenergy.com](http://www.nomiaenergy.com)
_© 2024 Nomia Energy_
"""

# Para cargar la configuracion del entorno (puerto, db, idiomas, etc)
load_dotenv()

AZURE_TRANSLATOR_KEY = os.getenv("7UuH0Sh8l7Hal5QriNH3mfdZ8YlMonk30UleUj8HkZbEkDJoucGWJQQJ99BCAC5T7U2XJ3w3AAAbACOGlNaw")
AZURE_TRANSLATOR_ENDPOINT = os.getenv("https://api.cognitive.microsofttranslator.com/")
AZURE_TRANSLATOR_REGION = os.getenv("francecentral")

# translator_client = TextTranslationClient(
#     credential=AzureKeyCredential(AZURE_TRANSLATOR_KEY),
#     endpoint=AZURE_TRANSLATOR_ENDPOINT
# )

# Añadir el directorio raíz al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejador de eventos de ciclo de vida."""
    # Código que se ejecuta en el startup
    await check_database_connection_workers()
    await check_database_connection_users()
    print("Conexión a la base de datos verificada")
    yield  # Aquí se ejecuta la aplicación
    # Código que se ejecuta en el shutdown (opcional)
    print("Aplicación cerrada correctamente")
    
# Configuración de FastAPI
app = FastAPI(
    title="SANTRA™ Me API",
    description=description,
    version=config.VERSION,
    lifespan=lifespan
)

# Incluir las rutas
app.include_router(api_mainRouter, prefix="/mainRoutes", tags=["Main Routes"])
app.include_router(api_sampleRouter, prefix="/sampleRoutes", tags=["Sample Routes"])
app.include_router(api_userRouter, prefix="/userRoutes", tags=["User Routes"])
app.include_router(api_workerRouter, prefix="/workerRoutes", tags=["Worker Routes"])
app.include_router(api_azureRouter, prefix="/azureRoutes", tags=["Azure Routes"])

# Monta el directorio estático
# app.mount("/static", StaticFiles(directory="src/Public/static"), name="static")
# Configura el directorio de plantillas
# templates = Jinja2Templates(directory=["src/Views/layouts", "src/Public/static"])

# Obtener la base del path, útil para compatibilidad con ejecutables
def get_base_path():
    if getattr(sys, 'frozen', False):  # Si es un ejecutable generado con PyInstaller
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

# Definimos BASE_PATH y STATIC_PATH
BASE_PATH = get_base_path()
STATIC_PATH = os.path.join(BASE_PATH, "src/Public/static")

# Monta el directorio estático usando STATIC_PATH
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

# Configura el directorio de plantillas usando BASE_PATH
templates = Jinja2Templates(directory=[
    os.path.join(BASE_PATH, "src/Views/layouts"),
    STATIC_PATH
])

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de compresión
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Configuración de colorlog para el formato de los logs
class HTTPStatusColorFormatter(colorlog.ColoredFormatter):
    def format(self, record):
        # Determinar el color según el código de estado HTTP
        if hasattr(record, 'status_code'):
            status = record.status_code
            color = 32  # Default green
            background_color = 107 # background white
            if status >= 500:
                color = 31  # Red for 5xx
                background_color = 107 # background white
            elif status >= 400:
                color = 33  # Yellow for 4xx
                background_color = 107 # background white
            elif status >= 300:
                color = 33  # Yellow for 3xx
                background_color = 107 # background white

            # Aplica el color al código de estado
            record.status_code_color = f"\x1b[{color};{background_color}m{status}\x1b[0m"
        else:
            record.status_code_color = ""
        
        # Llama al formatter base para que incluya la información normal (nivel, fecha, etc.)
        return super().format(record)

# Configuración del logger con color para niveles de log
handler = colorlog.StreamHandler()

logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG) # DEBUG muestra info detallada
# Puedo cambiar el nivel: 
# CRITICAL solo muestra los errores mas graves, ERROR errores importantes, 
# WARNING advertencias sobre posibles problemas, INFO informacion general sobre el funcionamiento del servidor (valor por defecto)
# DEBUG informacion detallada de depuracion

# Código de color ANSI
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
WHITE   = "\033[37m"
CYAN    = "\033[36m"
RESET   = "\033[0m"  # Resetear color al final del mensaje

# Middleware para registrar detalles de la solicitud HTTP -> duracion solicitud y otros detalles
@app.middleware("http")
async def log_request(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000)

    # Determinar color según el código de estado HTTP
    if response.status_code >= 500: # errores del servidor
        status_color = RED
    elif response.status_code >= 400: # errores del cliente
        status_color = RED
    elif response.status_code >= 300: # redirecciones
        status_color = YELLOW
    else:
        status_color = GREEN # color verde para codigos 2xx, exito

    # Obtener el mensaje asociado al código de estado
    status_message = HTTPStatus(response.status_code).phrase

    # Obtener la fecha y hora actual en el formato deseado
    current_time = datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    remote_ip = request.headers.get('X-Real-IP', request.client.host)
    full_url = request.url
    content_length = response.headers.get('Content-Length', 'Not Known')
    user = request.headers.get('X-User', 'Anonimous')

    log_message = (
        f"{GREEN}|santra-core-service | {CYAN}--------------------------------------------\n"
        f"{GREEN}|santra-core-service | {WHITE}[{current_time}] - {GREEN}{request.method} "
        f"{status_color}{response.status_code} {status_message}{RESET} "
        f"{CYAN}{request.url} {WHITE}- {duration_ms} ms - {remote_ip} - "
        f"{CYAN}{user}{WHITE} - {request.headers.get('user-agent', 'Anonimous')}{RESET} "
        f"Content-Length: {content_length}"
    )

    logger.info(log_message)
    return response

# Conexión a MongoDB
def check_mongo_connection():
    try:
        client = MongoClient('mongodb://root:example@localhost:27017')
        print("Conexión a MongoDB exitosa.")
    except Exception as e:
        print(f"Error de conexión a MongoDB: {e}")

# @app.post("/translate/")
# async def translate_text(request: Request, text: str, to_lang: str = "es"):
#     try:
#         translation_response = translator_client.translate(
#             content=[text], to=[to_lang], from_parameter="en"
#         )
#         translated_text = translation_response[0].translations[0].text
#         return JSONResponse(content={"translated_text": translated_text})
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})

# @app.route('/translate', methods=['POST'])
# def index_post():
#     original_text = request.form['text']
#     target_language = request.form['language']
#     key = os.environ['AZURE_TRANSLATOR_KEY']
#     endpoint = os.environ['AZURE_TRANSLATOR_ENDPOINT']
#     location = os.environ['AZURE_TRANSLATOR_REGION']
#     path = '/translate?api-version=3.0'
#     target_language_parameter = '&to=' + target_language
#     constructed_url = endpoint + path + target_language_parameter
#     headers = {
#         'Ocp-Apim-Subscription-Key': key,
#         'Ocp-Apim-Subscription-Region': location,
#         'Content-type': 'application/json',
#         'X-ClientTraceId': str(uuid.uuid4())
#     }
#     body = [{ 'text': original_text }]
#     translator_request = requests.post(constructed_url, headers=headers, json=body)
#     translator_response = translator_request.json()
#     translated_text = translator_response[0]['translations'][0]['text']
#     return render_template(
#         'results.html',
#         translated_text=translated_text,
#         original_text=original_text,
#         target_language=target_language
#     )

# Capturas excepciones no controladas. Para capturar y registrar errores globalmente.
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

# Redireccionar /privacidad a `privacidad.html`
# include_in_schema=False evita que esa ruta se muestre en /docs y /redoc
@app.get("/privacidad", response_class=HTMLResponse, include_in_schema=False)
async def render_privacidad(request: Request):
    return templates.TemplateResponse("privacidad.html", {
        "request": request,
        "version": config.VERSION,
        "environ": os.getenv('ENVIRONMENT'),
        "current_year": datetime.date.today().year
    })

# Redireccionar /distribucion a `distribucion.html`
# include_in_schema=False evita que esa ruta se muestre en /docs y /redoc
@app.get("/distribucion", response_class=HTMLResponse, include_in_schema=False)
async def render_distribucion(request: Request):
    return templates.TemplateResponse("distribucion.html", {
        "request": request,
        "version": config.VERSION,
        "environ": os.getenv('ENVIRONMENT'),
        "current_year": datetime.date.today().year
    })

@app.get("/hello", response_class=HTMLResponse, include_in_schema=False)
async def render_hello(request: Request):
    return templates.TemplateResponse("hello.html", {
        "request": request
    })

# Ruta principal que devuelve el HTML de `main.html`
# include_in_schema=False evita que esa ruta se muestre en /docs y /redoc
@app.get("/main", response_class=HTMLResponse, include_in_schema=False)
async def main(request: Request):    
    dic = request.state.dic
    return templates.TemplateResponse("main.html", {
        "request": request,
        "dic": dic,
        "version": config.VERSION,
        "environ": os.getenv('ENVIRONMENT'),
        "current_year": datetime.date.today().year
    })

# Redirigir todas las rutas a /main, excepto /docs y /redoc
@app.get("/{path_name:path}", include_in_schema=False)
async def catch_all(path_name: str):
    if path_name.startswith("docs") or path_name.startswith("redoc") or path_name.startswith("hello"):
        return RedirectResponse(url=f"/{path_name}")  # Permitir el acceso a /docs y /redoc
    return RedirectResponse(url="/main")

# Middleware para cargar diccionarios de idiomas
@app.middleware("http")
async def load_translations(request: Request, call_next):
    language = await get_current_language(request)
    try:
        request.state.dic = load_dictionary(language)
    except FileNotFoundError:
        request.state.dic = load_dictionary(DEFAULT_LANGUAGE)
    
    response = await call_next(request)
    return response

# Obtener idioma de la URL
async def get_current_language(request: Request):
    """
    Obtiene el lenguaje actual a partir de los parámetros en la URL.
    """
    language = request.query_params.get('lang', DEFAULT_LANGUAGE)
    if language in SUPPORTED_LANGUAGES:
        return language
    else:
        return DEFAULT_LANGUAGE

# Manejo de errores 404
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(status_code=404, content={"error": "Ruta NO encontrada", "code": 404})

# Configuración SSL para producción
def get_ssl_context():
    try:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(
            certfile=config.CRT_PATH,
            keyfile=config.KEY_PATH
        )
        return ssl_context
    except ssl.SSLError as e:
        raise RuntimeError(f"Error al cargar SSL: {e}")

# Iniciar la aplicación
# if __name__ == "__main__":
#     uvicorn.run(
#         app, 
#         host=config.DB_HOST, 
#         port=config.PORT, 
#         #log_level="warning",  # Configura el nivel de log
#         access_log=False,      # Desactiva el log de acceso
#         ssl_keyfile=config.KEY_PATH,
#         ssl_certfile=config.CRT_PATH,
#     )

# @app.on_event("startup")
# async def startup_event():
#     """Evento de inicio para verificar la conexión a la base de datos."""
#     await check_database_connection_workers()
#     await check_database_connection_users()

def get_resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso en el ejecutable empaquetado."""
    try:
        # PyInstaller guarda los recursos en _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Durante el desarrollo (sin PyInstaller), usa las rutas normales
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":

    # Verificar certificados para modo produccion
    # print(f"Certificado: {config.CRT_PATH}")
    # print(f"Clave: {config.KEY_PATH}")
    
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        os.chdir(sys._MEIPASS)

    if config.ENVIRONMENT == "production":
        uvicorn.run(
            app, 
            host=config.HOST, 
            port=config.PORT, 
            access_log=False,  # Desactiva el log de acceso
            ssl_keyfile=config.KEY_PATH,
            ssl_certfile=config.CRT_PATH
        )
    else:
        uvicorn.run(
            app,
            host=config.HOST,
            port=config.PORT,
            access_log=False
        )
