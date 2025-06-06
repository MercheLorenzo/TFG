"""
sampleRoutes.py

Este archivo define las rutas relacionadas con funcionalidades generales y utilidades en la aplicación. Utiliza FastAPI para calcular la suma de dos números, obtener la hora actual, generar cadenas aleatorias, obtener información meteorológica, y gestionar tokens JWT.

Rutas:
- GET /sum: Calcula la suma de dos números pasados como parámetros en la URL.
- GET /get-current-time: Obtiene la hora y fecha actual del servidor en UTC.
- GET /get-current-time-cet: Obtiene la hora y fecha actual del servidor en la zona horaria de España (CET).
- GET /generate-random-string: Genera una cadena aleatoria de longitud especificada por el usuario (por defecto 10 caracteres).
- GET /get-weather: Simula la obtención de información sobre la temperatura y funcionamiento de una caldera o sala.
- POST /generate-token: Genera un token JWT simulado.
- POST /verify-token: Verifica un token JWT simulado para comprobar su validez.

Cada ruta proporciona un resumen, descripción, y posibles códigos de respuesta para realizar operaciones generales de manera eficiente.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.Controllers.sampleController import generate_token, verify_token, sum_numbers, get_current_time, get_current_time_cet, generate_random_string, get_weather, TokenRequest, VerifyTokenRequest
from src.Models.sampleModels import TokenRequest, VerifyTokenRequest 

sampleRouter = APIRouter()

# Ruta para calcular la suma de dos numeros (GET)
# Esta ruta recibe dos números como parámetros de URL y devuelve su suma
@sampleRouter.get("/sum", summary="Calculates the sum of two numbers", description="Calculates the sum of two numbers passed as parameters in the URL", responses={
    200: {"description": "Sum calculated successfully"},
    400: {"description": "Error - invalid input, numbers required"},
    500: {"description": "Internal Server Error"},
})
async def sum_numbers_route(num1: float = None, num2: float = None):
    return await sum_numbers(num1, num2)

# Obtener la hora actual del servidor (GET)
# Devuelve la hora y fecha actuales del servidor
# UTC (España -2/-1 horas)
@sampleRouter.get("/get-current-time", summary="Get current server time (UTC)", description="Returns the current date and time of the server (UTC Time)", responses={
    200: {"description": "Current time obtained successfully"},
    500: {"description": "Internal Server Error"},
})
async def get_current_time_route():
    return await get_current_time()

# Obtener la hora actual del servidor (GET)
# Devuelve la hora y fecha actuales del servidor en la zona horaria de España
@sampleRouter.get("/get-current-time-cet", summary="Get current time in Spain (CET)", description="Returns the current date and time in Spain (CET)", responses={
    200: {"description": "Current time in Spain obtained successfully"},
    500: {"description": "Internal Server Error"},
})
async def get_current_time_cet_route():
    return await get_current_time_cet()

# Generar una cadena aleatoria (GET)
# Genera una cadena de texto aleatoria de longitud especificada por el usuario, útil para generar contraseñas o tokens
@sampleRouter.get("/generate-random-string", summary="Generate random string", description="Generates a random string of user-specified length, useful for generating passwords or tokens (default length is 10)", responses={
    200: {"description": "Random string generated successfully"},
    500: {"description": "Internal Server Error"},
})
async def generate_random_string_route(length: int = 10):
    return await generate_random_string(length)

# Obtener la temperatura y funcionamiento de una caldera/sala (simulado) (GET)
@sampleRouter.get("/get-weather", summary="Get boiler/room information", description="Simulates obtaining the temperature/operation of a boiler/room", responses={
    200: {"description": "Weather information obtained successfully"},
    500: {"description": "Internal Server Error"},
})
async def get_weather_route(room: str = "Sala 0"):
    return await get_weather(room)

# Generar un token JWT (POST)
@sampleRouter.post("/generate-token", summary="Generate JWT token", description="Generates a simulated JWT token", response_model=dict)
async def generate_token_route(request: TokenRequest):
    return await generate_token(request)

# Verificar un token JWT (POST)
@sampleRouter.post("/verify-token", summary="Verify JWT token", description="Verifies a simulated JWT token to check if a JWT token is valid", response_model=dict)
async def verify_token_route(request: VerifyTokenRequest):
    return await verify_token(request)
