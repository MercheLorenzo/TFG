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
from pymongo.errors import ServerSelectionTimeoutError
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
    azure_collection = db['tempazure']
except PyMongoError as e:
    raise e

# Pydantic model para trabajador
class Azure(BaseModel):

    email: Indexed(EmailStr, unique=True) = Field(..., description="Correo electrónico único del usuario")
    firstName: str = Field(..., max_length=50, description="Nombre del usuario (máximo 50 caracteres)") # description sale en la documentacion (swagger)
    lastName: str = Field(..., max_length=50, description="Apellido del usuario (máximo 50 caracteres)")

    # Esto es necesario para convertir el campo ObjectId en un tipo serializable (str)
    model_config = {
        "json_encoders": {ObjectId: str}
    }

class ImageDescription(BaseModel):
    user_email: EmailStr
    image_url: str  # o base64 si prefieres
    description: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Función para inicializar la base de datos
async def initialize_azure_db():
    """Crea la colección de trabajadores y el índice único en 'email' si no existen."""
    try:
        existing_collections = await db.list_collection_names()
        if 'tempazure' not in existing_collections:
            await db.create_collection('tempazure')
            debug_log("Colección 'tempazure' creada exitosamente.")
            print(f"{GREEN}|santra-c | {WHITE}[{current_time}] [ {CYAN}INFO{RESET} ] Successfully connected to Azure database.")

            # Crear índice único para el campo 'email'
            await azure_collection.create_index("email", unique=True)
            debug_log("Índice único en 'email' creado.")
        else:
            debug_log("La colección 'tempazure' ya existe.")
            print(f"{GREEN}|santra-c | {WHITE}[{current_time}] [ {CYAN}INFO{RESET} ] Successfully connected to Azure database.")
    except PyMongoError as e:
        print(f"{GREEN}|santra-c | {WHITE}[{current_time}] [ {CYAN}INFO{RESET} ] Couldn't connect to Azure database.")
        raise e