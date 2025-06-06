from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from src.Models.workerModel import Worker
from src.Controllers.workerController import (
    create_worker, get_worker_by_email, count_workers, search_workers
)

workerRouter = APIRouter()

# Crear un nuevo trabajador (POST)
# Esta ruta permite crear un nuevo trabajador en la base de datos
@workerRouter.post("/create-worker", response_model=Worker, summary="Create a new worker in the DB",
             description="Creates a new worker in the DB", responses={
                 201: {"description": "Worker created successfully"},
                 400: {"description": "Required fields missing"},
                 409: {"description": "A worker with this email already exists"},
                 500: {"description": "Internal Server Error"},
})
async def create_worker_route(worker: Worker):
    return await create_worker(worker)

# Obtener un trabajador por su correo electrónico (GET)
# Busca un trabajador en la base de datos a través de su correo electrónico
@workerRouter.get("/get-worker-by-email", response_model=Worker, summary="Get worker by email",
            description="Obtains a worker from the database by their email address", responses={
                200: {"description": "Worker found successfully"},
                400: {"description": "Email not provided"},
                404: {"description": "Worker not found"},
                500: {"description": "Internal Server Error"},
            })
async def get_worker_by_email_route(email: str):
    return await get_worker_by_email(email)

# Contar trabajadores totales en la base de datos (GET)
# Devuelve el número total de trabajadores almacenados
@workerRouter.get("/count-workers", summary="Count total workers", description="Counts the total number of workers present in the database", responses={
    200: {"description": "Worker count retrieved successfully"},
    500: {"description": "Internal Server Error"},
})
async def count_workers_route():
    return await count_workers()

# Buscar trabajadores en la base de datos (GET)
# Permite buscar trabajadores utilizando varios criterios
@workerRouter.get("/search-workers", response_model=List[Worker], summary="Search workers", description="Searches for workers by first or last name using partial matching", responses={
    200: {"description": "Workers found"},
    400: {"description": "Search query not provided"},
    404: {"description": "No workers found"},
    500: {"description": "Internal Server Error"},
})
async def search_workers_route(query: str):
    return await search_workers(query)