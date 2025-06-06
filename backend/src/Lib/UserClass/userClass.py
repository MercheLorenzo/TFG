""" 
userClass.py

Este archivo define la clase `UserClass`, que proporciona operaciones CRUD asincrónicas para la gestión de usuarios 
en una base de datos MongoDB usando el ODM Beanie. 

Funciones clave:
- **create**: Crea un nuevo usuario asegurando que el correo sea único y los nombres no excedan 50 caracteres.
- **get**: Recupera un usuario por su dirección de correo electrónico.

La clase utiliza validación de datos con Pydantic, gestión de errores con excepciones y logs informativos o de error 
para monitorear las operaciones realizadas.

El código es modular y está preparado para operaciones asincrónicas eficientes.
"""
from typing import List, Optional
from src.Models.userModel import User
from pydantic import ValidationError
from pymongo.errors import DuplicateKeyError
import logging

# Configurar logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("UserClass")

class UserClass:
    """
    Clase para operaciones CRUD sobre usuarios usando Beanie.
    """

    @staticmethod
    async def create(email: str, first_name: str, last_name: str) -> Optional[User]:
        """
        Crea un nuevo usuario en la base de datos, asegurándose de que los datos sean válidos.
        - El correo debe ser único.
        - Los nombres no deben exceder los 50 caracteres.
        """
        if len(first_name) > 50 or len(last_name) > 50:
            logger.error("El nombre o apellido supera los 50 caracteres.")
            raise ValueError("El nombre y el apellido no deben exceder los 50 caracteres.")

        try:
            existing_user = await User.find_one(User.email == email)
            if existing_user:
                logger.error(f"El correo electrónico {email} ya está en uso.")
                raise ValueError("El correo electrónico ya está en uso.")

            user = User(email=email, first_name=first_name, last_name=last_name)
            await user.insert()
            logger.info(f"Usuario creado: {user}")
            return user
        except ValidationError as ve:
            logger.error(f"Error de validación al crear usuario: {ve}")
            raise ve
        except Exception as e:
            logger.error(f"Error inesperado al crear usuario: {e}")
            raise e

    @staticmethod
    async def get(email: str) -> Optional[User]:
        """
        Obtiene un usuario por email.
        """
        try:
            user = await User.find_one(User.email == email)
            if user:
                logger.info(f"Usuario encontrado: {user}")
                return user
            logger.warning(f"No se encontró un usuario con el email: {email}")
            return None
        except Exception as e:
            logger.error(f"Error al buscar usuario: {e}")
            raise e
