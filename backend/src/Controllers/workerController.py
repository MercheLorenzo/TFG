from fastapi import HTTPException
from pydantic import EmailStr
from bson import ObjectId
from src.Models.workerModel import worker_collection
from typing import List, Optional
from src.Content.i18n import load_dictionary
from src.Models.workerModel import Worker
from datetime import datetime

# Código de color ANSI
RED     = "\033[31m"
GREEN   = "\033[32m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"
RESET   = "\033[0m"
current_time = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')  # Formato de fecha y hora

async def check_database_connection_workers():
    """Prueba la conexión a la base de datos al arrancar o para verificar problemas."""
    try:
        # Ejecuta una operación básica como `ping` o cuenta documentos
        await worker_collection.database.command("ping")
        print(f"{GREEN}|santra-c | {WHITE}[{current_time}] [ {GREEN}OK{RESET} ] Successfully connected to workers database.")
        return True
    except Exception as e:
        print(f"{GREEN}|santra-c | {WHITE}[{current_time}] [ {RED}ERROR{RESET} ] Couldn't connect to workers database.")
        # raise HTTPException(status_code=500, detail="Error de conexión con la base de datos de trabajadores")

# Crear un trabajador en la base de datos (POST)
async def create_worker(worker: Worker):
    existing_worker = await worker_collection.find_one({"email": worker.email})
    if existing_worker:
        raise HTTPException(status_code=409, detail="El trabajador con este correo ya existe")

    try:
        new_worker = worker.dict()
        result = await worker_collection.insert_one(new_worker)

        new_worker["_id"] = str(result.inserted_id)
        return new_worker
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear el trabajador: " + str(e))

# Buscar un trabajador por su correo electrónico (GET)
async def get_worker_by_email(email: str):
    try:
        worker = await worker_collection.find_one({"email": email})
        if not worker:
            raise HTTPException(status_code=404, detail="Trabajador no encontrado")
        worker["_id"] = str(worker["_id"])
        return worker
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Contar el número total de trabajadores en la base de datos (GET)
async def count_workers():
    try:
        count = await worker_collection.count_documents({})
        return {'total_workers': count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Buscar trabajadores por nombre o apellido parcial (GET)
async def search_workers(name: str):
    try:
        cursor = worker_collection.find({
            "$or": [
                {"firstName": {"$regex": name, "$options": "i"}},
                {"lastName": {"$regex": name, "$options": "i"}},
                {"secondLastName": {"$regex": name, "$options": "i"}}
            ]
        }, {'_id': 1, 'email': 1, 'firstName': 1, 'lastName': 1, 'secondLastName': 1})

        workers = await cursor.to_list(length=None)

        if not workers:
            raise HTTPException(status_code=404, detail="No workers found")

        for worker in workers:
            worker['_id'] = str(worker['_id'])

        return workers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))