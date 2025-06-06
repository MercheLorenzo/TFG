"""
mainRoutes.py

Este archivo define las rutas principales para la API, gestionando la información básica sobre el estado del servidor, la versión de la API y ejemplos de errores. Utiliza FastAPI para manejar las peticiones GET y proporcionar respuestas sobre el estado y la versión del sistema, además de simular respuestas de error.

Rutas:
- GET /get-status: Devuelve el estado actual del servidor, indicando si está funcionando correctamente.
- GET /get-version: Proporciona la versión y el entorno de la API, con soporte para varios idiomas (es, en, fr, it, de, ch).
- GET /get-error-sample: Devuelve un ejemplo de respuesta de error para ilustrar cómo se maneja un error en la API.

Cada ruta proporciona un resumen, descripción, y posibles códigos de respuesta para realizar operaciones generales y obtener información sobre el estado del servidor y la versión de la API.
"""
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from src.Config.config import config
from src.Content.i18n import load_dictionary, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE
from src.Controllers.mainController import get_status, get_version, get_error_sample  # Importar funciones del controlador

mainRouter = APIRouter()

@mainRouter.get("/get-status", summary="Returns the server status", description="Check the server status", responses={
    200: {"description": "OK - The server is running"},
    500: {"description": "Internal Server Error"}
})
async def route_get_status():
    return await get_status()

@mainRouter.get("/get-version", summary="Returns the API version", description="Returns the version and environment of the application, with translations (es, en, fr, it, de, ch)", responses={
    200: {"description": "OK - Successful operation"},
    500: {"description": "Internal Server Error"}
})
async def route_get_version(request: Request, lang: str = DEFAULT_LANGUAGE):
    return await get_version(request, lang)

@mainRouter.get("/get-error-sample", summary="Error response example", description="Returns an example of an error response", responses={
    400: {"description": "Error Sample"},
    500: {"description": "Internal Server Error"}
})
async def route_get_error_sample():
    return await get_error_sample()
