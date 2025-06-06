"""
sampleController.py

Este archivo proporciona ejemplos prácticos que demuestran diversas funcionalidades que se pueden implementar en una API. 
Incluye operaciones matemáticas, generación de datos simulados, manejo de fechas y gestión de tokens JWT.

**Resumen de funcionalidades**:
1. **`sum_numbers`** (GET): 
   - Suma dos números proporcionados y devuelve el resultado.  
   - Maneja validaciones simples para la entrada.

2. **`get_current_time`** (GET):  
   - Devuelve la hora actual en formato UTC.

3. **`get_current_time_cet`** (GET):  
   - Devuelve la hora actual ajustada al huso horario CET (Europa/Madrid).

4. **`generate_random_string`** (GET):  
   - Genera una cadena de texto aleatoria con longitud configurable (por defecto 10 caracteres).

5. **`get_weather`** (GET):  
   - Simula el estado de una sala/caldera, devolviendo valores fijos como temperatura y humedad.

6. **`generate_token`** (POST):  
   - Genera un **token JWT** con un tiempo de expiración basado en un nombre de usuario recibido como parámetro.

7. **`verify_token`** (POST):  
   - Verifica y decodifica un token JWT, devolviendo el nombre de usuario si el token es válido.  
   - Maneja errores de token expirado o inválido.

**Uso principal**:
Este módulo sirve como referencia para mostrar cómo manejar operaciones comunes en una API, como cálculos, simulación de datos, control de fechas/tiempo y autenticación con JWT.
"""
from fastapi import HTTPException
from datetime import datetime, timedelta
import pytz
import string
import random
import jwt
from src.Config.config import config
from pymongo import MongoClient
from bson import ObjectId
from src.Models.sampleModels import TokenRequest, VerifyTokenRequest 

# Clave secreta a usar luego en unas rutas de crear y verificar tokens
SECRET_KEY = config.SECRET_KEY  # Usando variable de configuración

# Sumar dos numeros
async def sum_numbers(num1: float, num2: float):
    if num1 is None or num2 is None:
        raise HTTPException(status_code=400, detail="Invalid input, numbers required")
    result = num1 + num2
    return {"num1": num1, "num2": num2, "sum": result}

# Tiempo/Fecha UTC
async def get_current_time():
    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    return {"current_time": current_time}

# Fecha CET (España)
async def get_current_time_cet():
    timezone = pytz.timezone('Europe/Madrid')
    current_time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
    return {"current_time": current_time}

# Generar string random, longitud por defecto es de 10, se puede cambiar
async def generate_random_string(length: int = 10):
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return {"random_string": random_string}

# Obtener temperatura de una sala/caldera (simulado, pongas el nombre que pongas, te dara el mismo resultado)
async def get_weather(room: str = "Sala 0"):
    weather_info = {
        "room": room,
        "temperature": "25 degrees",
        "conditions": "NOT WORKING, need reparation",
        "humidity": "40%"
    }
    return weather_info

# Generar token usando la secret key
async def generate_token(request: TokenRequest):
    if not request.username:
        raise HTTPException(status_code=400, detail="No username provided")

    # Crear el token
    token = jwt.encode({
        'username': request.username,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, SECRET_KEY, algorithm='HS256')

    return {"token": token}

# Verificar token
async def verify_token(request: VerifyTokenRequest):
    if not request.token:
        raise HTTPException(status_code=400, detail="No token provided")

    try:
        decoded = jwt.decode(request.token, SECRET_KEY, algorithms=['HS256'])
        return {"username": decoded['username']}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
