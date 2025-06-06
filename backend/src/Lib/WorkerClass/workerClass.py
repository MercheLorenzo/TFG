from typing import List, Optional
from src.Models.workerModel import Worker
from pydantic import ValidationError
from pymongo.errors import DuplicateKeyError
import logging

# Configurar logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WorkerClass")

class WorkerClass:
    """
    Clase para operaciones CRUD sobre trabajadores usando Beanie.
    """

    @staticmethod
    async def create(email: str, first_name: str, last_name: str) -> Optional[Worker]:
        """
        Crea un nuevo trabajador en la base de datos, asegurándose de que los datos sean válidos.
        - El correo debe ser único.
        - Los nombres no deben exceder los 50 caracteres.
        """
        if len(first_name) > 50 or len(last_name) > 50:
            logger.error("El nombre o apellido supera los 50 caracteres.")
            raise ValueError("El nombre y el apellido no deben exceder los 50 caracteres.")

        try:
            existing_worker = await Worker.find_one(Worker.email == email)
            if existing_worker:
                logger.error(f"El correo electrónico {email} ya está en uso.")
                raise ValueError("El correo electrónico ya está en uso.")

            worker = Worker(email=email, first_name=first_name, last_name=last_name)
            await worker.insert()
            logger.info(f"Trabajador creado: {worker}")
            return worker
        except ValidationError as ve:
            logger.error(f"Error de validación al crear trabajador: {ve}")
            raise ve
        except Exception as e:
            logger.error(f"Error inesperado al crear trabajador: {e}")
            raise e

    @staticmethod
    async def get(email: str) -> Optional[Worker]:
        """
        Obtiene un trabajador por email.
        """
        try:
            worker = await Worker.find_one(Worker.email == email)
            if worker:
                logger.info(f"Trabajador encontrado: {worker}")
                return worker
            logger.warning(f"No se encontró un trabajador con el email: {email}")
            return None
        except Exception as e:
            logger.error(f"Error al buscar trabajador: {e}")
            raise e
