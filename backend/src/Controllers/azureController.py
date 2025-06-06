import httpx
import os
from fastapi import HTTPException
from pydantic import EmailStr
from bson import ObjectId
from src.Models.azureModel import azure_collection
from typing import List, Optional
from src.Content.i18n import load_dictionary
from src.Models.azureModel import Azure,ImageDescription
from datetime import datetime

AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY")

# Código de color ANSI
RED     = "\033[31m"
GREEN   = "\033[32m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"
RESET   = "\033[0m"
current_time = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')  # Formato de fecha y hora

async def check_database_connection_azure():
    """Prueba la conexión a la base de datos al arrancar o para verificar problemas."""
    try:
        # Ejecuta una operación básica como `ping` o cuenta documentos
        await azure_collection.database.command("ping")
        print(f"{GREEN}|santra-c | {WHITE}[{current_time}] [ {GREEN}OK{RESET} ] Successfully connected to Azure database.")
        return True
    except Exception as e:
        print(f"{GREEN}|santra-c | {WHITE}[{current_time}] [ {RED}ERROR{RESET} ] Couldn't connect to Azure database.")
        # raise HTTPException(status_code=500, detail="Error de conexión con la base de datos de trabajadores")

# Crear un trabajador en la base de datos (POST)
async def create_azure(worker: Azure):
    existing_worker = await azure_collection.find_one({"email": worker.email})
    if existing_worker:
        raise HTTPException(status_code=409, detail="El trabajador con este correo ya existe")

    try:
        new_worker = worker.dict()
        result = await azure_collection.insert_one(new_worker)

        new_worker["_id"] = str(result.inserted_id)
        return new_worker
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear el trabajador de azure: " + str(e))

# Buscar un trabajador por su correo electrónico (GET)
async def get_azure_by_email(email: str):
    try:
        worker = await azure_collection.find_one({"email": email})
        if not worker:
            raise HTTPException(status_code=404, detail="Trabajador azure no encontrado")
        worker["_id"] = str(worker["_id"])
        return worker
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Contar el número total de trabajadores en la base de datos (GET)
async def count_azure():
    try:
        count = await azure_collection.count_documents({})
        return {'total_workers': count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Buscar trabajadores por nombre o apellido parcial (GET)
async def search_azure(name: str):
    try:
        cursor = azure_collection.find({
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
    
async def describe_image(image_data: ImageDescription):
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_VISION_KEY,
        "Content-Type": "application/json"
    }
    body = {"url": image_data.image_url}
    params = {"visualFeatures": "Description"}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{AZURE_VISION_ENDPOINT}/vision/v3.2/analyze",
                headers=headers,
                params=params,
                json=body
            )
            response.raise_for_status()
            data = response.json()
            caption = data["description"]["captions"][0]["text"] if data["description"]["captions"] else "No description found."

            # Guardar en MongoDB (colección nueva o embebida en el usuario)
            record = image_data.dict()
            record["description"] = caption
            await db["image_descriptions"].insert_one(record)

            return {"description": caption}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando imagen: {str(e)}")