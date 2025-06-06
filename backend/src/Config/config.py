"""
config.py

Este archivo gestiona la configuración global de la aplicación utilizando Pydantic BaseSettings y variables de entorno:
- Carga variables desde archivos `.env` o desde el entorno global del sistema.
- Contiene parámetros esenciales como la versión, entorno, nombres y puertos de servicios, credenciales de la base de datos, y claves secretas.
- Incluye lógica auxiliar, como `get_git_version` para recuperar etiquetas de versión desde Git.
- Muestra información en la consola, como confirmación de entorno, base de datos y puerto activo.
- Permite mantener entornos consistentes entre desarrollo y producción, asegurando valores predeterminados cuando variables no están definidas.
"""
import os
import ssl
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from datetime import datetime
from typing import List
import subprocess
from src.Lib.helpers.nomia_utils import debug_log

# Para obtener la version de git (git describe --tags) 
# Para cambiarla, haz "git tag v1.0.05" "git push origin v1.0.05"
def get_git_version():
    try:
        return subprocess.check_output(["git", "describe", "--tags"]).strip().decode('utf-8')
    except Exception:
        return 'v1.0.0'  # Valor por defecto si no hay tag

# Cargar el archivo .env específico si ENV_FILE está definido
env_file = os.getenv("ENV_FILE")  # Usa .env por defecto si no se pasa otro archivo
load_dotenv(env_file, override=True)  # Carga el archivo .env especificado

# Código de color ANSI
GREEN   = "\033[32m"
CYAN = "\033[36m"
WHITE   = "\033[37m"
RESET = "\033[0m"  # Resetear color al final del mensaje # WHITE, blanco

# Verificación de carga con fecha
current_time = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')  # Formato de fecha y hora
print(f"{GREEN}|santra-c |{RESET} -------------------------------------------------------------------------------------------")
print(f"{GREEN}|santra-c |{RESET}                    {CYAN}Santra™ Core Template Service v.1.0.0{RESET} - Build 0")
print(f"{GREEN}|santra-c |{RESET} -------------------------------------------------------------------------------------------")
print(f"{GREEN}|santra-c | {WHITE}[{current_time}]{RESET} [ {GREEN}OK{RESET} ] Loaded environment from {env_file}")
print(f"{GREEN}|santra-c | {WHITE}[{current_time}]{RESET} [ {GREEN}OK{RESET} ] Current environment is Env: {os.getenv('ENVIRONMENT')}")
print(f"{GREEN}|santra-c | {WHITE}[{current_time}]{RESET} [ {GREEN}OK{RESET} ] Santra Service Started at Port {os.getenv('PORT')}")
debug_log(f"{GREEN}|santra-c | {WHITE}[{current_time}]{RESET} [ {GREEN}OK{RESET} ] Database: {os.getenv('DB')}")

class Config(BaseSettings):
    VERSION: str = get_git_version()
    BUILD: str = datetime.now().strftime('%d-%m-%Y') # Fecha de construcción/build
    SERVICE_NAME: str = 'FastAPI Microservice, Nomia Energy' # Nombre del servicio
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')    
    NODE_ENV: str = os.getenv('NODE_ENV', 'test')
    INSTANCE_ID: str = os.getenv('INSTANCE_ID', 'main')
    TEST_LOGS: bool = os.getenv('TEST_LOGS', 'false').lower() == 'true'
    SECRET_TEST: str = os.getenv('SECRET_TEST', 'Not defined in Environment')
    BASE_API: str = os.getenv('BASE_API', '/docs')
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'supersecretkey') # Clave secreta para generar tokens (un par de rutas de la api)
    PORT: int = int(os.getenv('PORT', 8000))
    HOST: str = os.getenv('HOST', '0.0.0.0')  # Dirección IP para escuchar conexiones
    DB: str = os.getenv('DB', 'mongodb://172.29.80.1:27017/microservice') # DB en localhost ; mongodb://localhost:27017/development ; mongodb://santra-database:27017/microservice
    DB_HOST: str = os.getenv('DB_HOST', '172.29.80.1')
    DB_PORT: int = int(os.getenv('DB_PORT', 27017))
    DB_NAME: str = os.getenv('DB_NAME', 'microservice')
    SUPPORTED_LANGUAGES: List[str] = os.getenv('SUPPORTED_LANGUAGES', 'es,en,fr,it,de,ch').split(',') or ['es', 'en', 'fr', 'it', 'de', 'ch']
    DEFAULT_LANGUAGE: str = os.getenv('DEFAULT_LANGUAGE', 'es')
    CRT_PATH: str = os.path.abspath(os.getenv('CRT_PATH', './src/Config/santracli.crt'))
    KEY_PATH: str = os.path.abspath(os.getenv('KEY_PATH', './src/Config/santracli.key'))
    CA_PATH: str = os.getenv('CA_PATH', '')
    AZURE_TRANSLATOR_KEY: str = os.getenv('AZURE_TRANSLATOR_KEY', '7UuH0Sh8l7Hal5QriNH3mfdZ8YlMonk30UleUj8HkZbEkDJoucGWJQQJ99BCAC5T7U2XJ3w3AAAbACOGlNaw')
    AZURE_TRANSLATOR_ENDPOINT: str = os.getenv('AZURE_TRANSLATOR_ENDPOINT', 'https://api.cognitive.microsofttranslator.com/')
    AZURE_TRANSLATOR_REGION: str = os.getenv('AZURE_TRANSLATOR_REGION', 'francecentral')

# Cargar la configuración actual
config = Config()