"""
sample_class.py

Clase para manejar datos de 'Sample' utilizando Pydantic y MongoDB.

Define un modelo de entrada de datos (CreateSampleInput) con validación de campos.
La clase 'SampleClass' proporciona métodos para acceder, modificar y guardar muestras en la base de datos.
Implementa operaciones asincrónicas para interactuar con MongoDB a través de motor AsyncIOMotorClient.
Permite insertar nuevos documentos o actualizar existentes en la colección 'samples'.
Incluye métodos para convertir los objetos de la clase a diccionarios y recuperar datos desde la base de datos.
"""
from pydantic import BaseModel, EmailStr, Field, ValidationError
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# Modelo Pydantic para la entrada de datos de Sample
class CreateSampleInput(BaseModel):
    email: EmailStr = Field(..., min_length=7, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)

# Clase para trabajar con el modelo Sample
class SampleClass:
    def __init__(self, input_data: CreateSampleInput):
        self._email = input_data.email
        self._first_name = input_data.first_name
        self._last_name = input_data.last_name

    @property
    def email(self) -> str:
        return self._email

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @email.setter
    def email(self, value: str):
        self._email = value

    @first_name.setter
    def first_name(self, value: str):
        self._first_name = value

    @last_name.setter
    def last_name(self, value: str):
        self._last_name = value

    def as_dict(self) -> dict:
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

    async def save(self, db):
        collection = db.get_collection("samples")
        existing_sample = await collection.find_one({"email": self.email})
        
        if existing_sample:
            # Update existing document
            result = await collection.update_one(
                {"email": self.email},
                {"$set": self.as_dict()}
            )
            return await collection.find_one({"email": self.email})
        else:
            # Insert new document
            await collection.insert_one(self.as_dict())
            return await collection.find_one({"email": self.email})

    @staticmethod
    async def get_from_db(email: str, db):
        collection = db.get_collection("samples")
        sample = await collection.find_one({"email": email})
        return sample