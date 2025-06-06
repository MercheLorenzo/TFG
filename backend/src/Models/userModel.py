"""
userModel.py

Este archivo define los modelos de datos y la configuración de la base de datos MongoDB para la gestión de usuarios. 
Utiliza Pydantic para la validación de datos y Motor como cliente asincrónico de MongoDB.

Modelos principales:
- **User**: Modelo base que representa un usuario con validación de correo único, nombre y apellido.
- **UpdateEmailDomain**: Modelo para actualizar el dominio del correo electrónico de un usuario.
- **UserUpdate**: Permite la actualización de datos del usuario con campos opcionales.

Funciones:
- **initialize_users_db**: Inicializa la colección 'tempusers' en la base de datos con un índice único en el campo 'email'.

Se incluyen logs detallados y gestión de errores para una inicialización segura y trazabilidad de los datos.
"""
from beanie import Document, Indexed, init_beanie
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from typing import List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from src.Config.config import config
import json
from pymongo.errors import DuplicateKeyError, PyMongoError
from src.Lib.helpers.nomia_utils import debug_log
from beanie import Document, Indexed
import logging
import json
from datetime import datetime
import asyncio

# Código de color ANSI
GREEN   = "\033[32m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"
RESET   = "\033[0m"
current_time = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')  # Formato de fecha y hora

# Conexión a MongoDB para la colección de usuarios usando las variables del archivo de configuracion
MONGODB_URI = config.DB
DATABASE_NAME = config.DB_NAME

try:
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    users_collection = db['tempusers']
except PyMongoError as e:
    raise e

# Pydantic model para usuario
class User(BaseModel):
    # email: EmailStr
    # firstName: str
    # lastName: str

    # email: EmailStr = Field(..., unique=True, description="Correo electrónico único del usuario") # ... indica que el campo es obligatorio
    # unique=True:
    # Es una personalización, pero Pydantic no aplica restricciones directamente en la base de datos
    # Aunque lo incluyas en Field, tendrás que configurar la unicidad de manera explícita en MongoDB, como ya haces en la función initialize_users_db con create_index("email", unique=True)
    
    email: Indexed(EmailStr, unique=True) = Field(..., description="Correo electrónico único del usuario")
    firstName: str = Field(..., max_length=50, description="Nombre del usuario (máximo 50 caracteres)") # description sale en la documentacion (swagger)
    lastName: str = Field(..., max_length=50, description="Apellido del usuario (máximo 50 caracteres)")

    # Esto es necesario para convertir el campo ObjectId en un tipo serializable (str)
    model_config = {
        "json_encoders": {ObjectId: str}
    }

# Modelo para actualizar el dominio del correo electrónico
class UpdateEmailDomain(BaseModel):
    new_domain: str

# Modelo para actualizar la información del usuario (con campos opcionales)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None

# Función para inicializar la base de datos
async def initialize_users_db():
    """Crea la colección de usuarios y el índice único en 'email' si no existen."""
    try:
        existing_collections = await db.list_collection_names()
        if 'tempusers' not in existing_collections:
            await db.create_collection('tempusers')
            debug_log("Colección 'tempusers' creada exitosamente.")
            print(f"{GREEN}|santra-c | {WHITE}[{current_time}] [ {CYAN}INFO{RESET} ] Successfully connected to users database.")
            # Crear índice único para el campo 'email'
            await users_collection.create_index("email", unique=True)
            debug_log("Índice único en 'email' creado.")
        else:
            debug_log("La colección 'tempusers' ya existe.")
            print(f"{GREEN}|santra-c | {WHITE}[{current_time}] [ {CYAN}INFO{RESET} ] Successfully connected to users database.")
    except PyMongoError as e:
        print(f"{GREEN}|santra-c | {WHITE}[{current_time}] [ {CYAN}INFO{RESET} ] Couldn't connect to users database.")
        #raise e
    
