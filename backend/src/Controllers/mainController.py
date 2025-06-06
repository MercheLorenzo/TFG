"""
mainController.py

Este archivo define las rutas principales de la API y sus controladores asociados:
- Permite verificar el **estado del servidor** mediante una respuesta simple.
- Proporciona información sobre la **versión**, el entorno del servicio, y un mensaje de bienvenida adaptado al idioma solicitado.
- Incluye un ejemplo de manejo de **errores estructurados**, útil para pruebas y demostraciones.

**Resumen de funcionalidades**:
1. **`get_status`** (GET): Responde con el estado "OK", confirmando que el servidor está activo.
2. **`get_version`** (GET): 
   - Devuelve la versión del servicio, entorno de ejecución y un mensaje localizado de bienvenida.
   - Carga las traducciones utilizando `i18n.py` según el idioma especificado en los parámetros.
3. **`get_error_sample`** (GET): Devuelve un ejemplo de estructura de error predefinida, mostrando cómo manejar respuestas de error personalizadas.

Este archivo sirve como **punto de entrada** principal para comprobaciones generales del servidor y configuración básica.
"""
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from src.Config.config import config
from src.Content.i18n import load_dictionary, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE

# Get status del servidor
async def get_status():
    return JSONResponse(content={"response": "OK"}, status_code=200)

# Get version -> informacion de la version, entorno y mensaje de bienvenida en el idioma seleccionado
async def get_version(request: Request, lang: str = DEFAULT_LANGUAGE):
    # Verificar y establecer el idioma
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE

    # Cargar el diccionario basado en el idioma especificado
    try:
        dic = load_dictionary(lang)
    except FileNotFoundError:
        dic = load_dictionary(DEFAULT_LANGUAGE)  # Cargar el diccionario por defecto si hay un error -> por defecto ESPAÑOL

    if not dic:
        raise HTTPException(status_code=500, detail="Diccionario no cargado correctamente")

    # Información de la versión
    version_info = {
        "response": f"{config.VERSION} - {config.ENVIRONMENT}",
        "message": f"{dic.get('content', {}).get('welcome', '¡Bienvenido!')} {dic.get('content', {}).get('servidor', 'Servidor Santra Me')}" # Mensaje de bienvenida en el idioma seleccionado
    }
    return JSONResponse(content=version_info, status_code=200)

# Ejemplo de error
async def get_error_sample():
    error_response = {
        "error": {
            "code": "ERR_000",
            "message": "Demo Error",
            "category": "ERROR",
            "module": "main_routes.get_error_sample"
        }
    }
    return JSONResponse(content=error_response, status_code=400)
