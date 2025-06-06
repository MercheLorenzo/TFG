from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from src.Models.azureModel import Azure
from src.Controllers.azureController import (
    create_azure, get_azure_by_email, describe_image, count_azure, search_azure
)

azureRouter = APIRouter()

# Crear un nuevo trabajador (POST)
# Esta ruta permite crear un nuevo trabajador en la base de datos
@azureRouter.post("/create-azure", response_model=Azure, summary="Create a new worker in the DB",
             description="Creates a new worker in the DB", responses={
                 201: {"description": "Worker created successfully"},
                 400: {"description": "Required fields missing"},
                 409: {"description": "A worker with this email already exists"},
                 500: {"description": "Internal Server Error"},
})
async def create_azure_route(worker: Azure):
    return await create_azure(worker)

# Obtener un trabajador por su correo electrónico (GET)
# Busca un trabajador en la base de datos a través de su correo electrónico
@azureRouter.get("/get-azure-by-email", response_model=Azure, summary="Get worker by email",
            description="Obtains a worker from the database by their email address", responses={
                200: {"description": "Worker found successfully"},
                400: {"description": "Email not provided"},
                404: {"description": "Worker not found"},
                500: {"description": "Internal Server Error"},
            })
async def get_azure_by_email_route(email: str):
    return await get_azure_by_email(email)

# Contar trabajadores totales en la base de datos (GET)
# Devuelve el número total de trabajadores almacenados
@azureRouter.get("/count-azure", summary="Count total workers", description="Counts the total number of workers present in the database", responses={
    200: {"description": "Worker count retrieved successfully"},
    500: {"description": "Internal Server Error"},
})
async def count_azure_route():
    return await count_azure()

# Buscar trabajadores en la base de datos (GET)
# Permite buscar trabajadores utilizando varios criterios
@azureRouter.get("/search-azure", response_model=List[Azure], summary="Search workers", description="Searches for workers by first or last name using partial matching", responses={
    200: {"description": "Workers found"},
    400: {"description": "Search query not provided"},
    404: {"description": "No workers found"},
    500: {"description": "Internal Server Error"},
})
async def search_azure_route(query: str):
    return await search_azure(query)

@azureRouter.post("/describe-image", summary="Describe an image using Azure Vision",
    description="Receives an image and returns a description using Azure Computer Vision API.",
    responses={
        200: {"description": "Image described successfully"},
        400: {"description": "Invalid image or bad request"},
        500: {"description": "Internal Server Error"},
    })
async def describe_image_route(image: UploadFile = File(...)):
    return await describe_image(image)