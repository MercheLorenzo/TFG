"""
userRoutes.py

Este archivo define las rutas relacionadas con la gestión de usuarios en la aplicación. Utiliza FastAPI para crear, obtener, contar, buscar y actualizar usuarios en la base de datos.

Rutas:
- POST /create-user: Crea un nuevo usuario en la base de datos.
- GET /get-user-by-email: Obtiene un usuario por su correo electrónico.
- GET /count-users: Devuelve el número total de usuarios en la base de datos.
- GET /search-users: Permite buscar usuarios por nombre o apellido mediante coincidencias parciales.
- PUT /update-user/{user_id}: (comentada) Actualiza los datos de un usuario existente.
- DELETE /delete-user/{user_id}: (comentada) Elimina un usuario de la base de datos.
- PUT /update-email-domain: (comentada) Actualiza el dominio del correo electrónico de todos los usuarios.

Cada ruta proporciona un resumen, descripción, y posibles códigos de respuesta para gestionar los usuarios de manera eficiente.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from src.Models.userModel import User, UserUpdate, UpdateEmailDomain
from src.Controllers.userController import (
    create_user, get_user_by_email, count_users, search_users
)

userRouter = APIRouter()

# Crear un nuevo usuario (POST)
# Esta ruta permite crear un nuevo usuario en la base de datos
@userRouter.post("/create-user", response_model=User, summary="Create a new user in the DB",
             description="Creates a new user in the DB", responses={
                 201: {"description": "User created successfully"},
                 400: {"description": "Required fields missing"},
                 409: {"description": "A user with this email already exists"},
                 500: {"description": "Internal Server Error"},
})
async def create_user_route(user: User):
    return await create_user(user)

# Obtener un usuario por su correo electrónico (GET)
# Busca un usuario en la base de datos a través de su correo electrónico
@userRouter.get("/get-user-by-email", response_model=User, summary="Get user by email",
            description="Obtains a user from the database by their email address", responses={
                200: {"description": "User found successfully"},
                400: {"description": "Email not provided"},
                404: {"description": "User not found"},
                500: {"description": "Internal Server Error"},
            })
async def get_user_by_email_route(email: str):
    return await get_user_by_email(email)

# Contar usuarios totales en la base de datos (GET)
# Devuelve el número total de usuarios almacenados
@userRouter.get("/count-users", summary="Count total users", description="Counts the total number of users present in the database", responses={
    200: {"description": "User count retrieved successfully"},
    500: {"description": "Internal Server Error"},
})
async def count_users_route():
    return await count_users()

# Buscar usuarios en la base de datos (GET)
# Permite buscar usuarios utilizando varios criterios
@userRouter.get("/search-users", response_model=List[User], summary="Search users", description="Searches for users by first or last name using partial matching", responses={
    200: {"description": "Users found"},
    400: {"description": "Search query not provided"},
    404: {"description": "No users found"},
    500: {"description": "Internal Server Error"},
})
async def search_users_route(query: str):
    return await search_users(query)

# Actualizar un usuario existente en la base de datos (PUT)
# Podemos actualizar los campos firstName, lastName o email
# @userRouter.put("/update-user/{user_id}", response_model=User, summary="Update a user in the DB",
#              description="Updates a user in the database", responses={
#                  200: {"description": "User updated successfully"},
#                  400: {"description": "No data to update"},
#                  404: {"description": "User not found"},
#                  500: {"description": "Internal Server Error"},
#              })
# async def update_user(user_id: str, user: UserUpdate):
#     try:
#         # Convertir el ID del usuario a ObjectId
#         obj_id = ObjectId(user_id)

#         # Filtrar solo los campos proporcionados que no sean None
#         updated_data = {k: v for k, v in user.dict().items() if v is not None}
#         if not updated_data:
#             raise HTTPException(status_code=400, detail="No hay datos para actualizar")

#         # Verificar si el usuario existe
#         existing_user = await users_collection.find_one({"_id": obj_id})
#         if not existing_user:
#             raise HTTPException(status_code=404, detail="Usuario no encontrado")

#         # Actualizar el usuario
#         await users_collection.update_one({"_id": obj_id}, {"$set": updated_data})

#         # Obtener el usuario actualizado
#         updated_user = await users_collection.find_one({"_id": obj_id})
#         updated_user["_id"] = str(updated_user["_id"])  # Convertir ObjectId a string para la respuesta

#         return updated_user
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# Eliminar un usuario de la base de datos (DELETE)
# @userRouter.delete("/delete-user/{user_id}", summary="Delete a user from the DB",
#                description="Deletes a user from the database by ID", responses={
#                    200: {"description": "User deleted successfully"},
#                    404: {"description": "User not found"},
#                    500: {"description": "Internal Server Error"},
#                })
# async def delete_user(user_id: str):
#     try:
#         # Convertir el ID del usuario a ObjectId
#         obj_id = ObjectId(user_id)

#         # Verificar si el usuario existe
#         user = await users_collection.find_one({"_id": obj_id})
#         if not user:
#             raise HTTPException(status_code=404, detail="Usuario no encontrado")

#         # Eliminar el usuario de la base de datos
#         await users_collection.delete_one({"_id": obj_id})

#         return {"message": f'Usuario con ID {user_id} eliminado exitosamente'}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# Actualizar el dominio del correo de todos los usuarios (PUT)
# @userRouter.put("/update-email-domain", summary="Update email domain", description="Updates the email domain of all users", responses={
#     200: {"description": "Email domain updated"},
#     400: {"description": "New domain not provided"},
#     500: {"description": "Internal Server Error"},
# })
# async def update_email_domain(domain: UpdateEmailDomain):
#     try:
#         new_domain = domain.new_domain

#         if not new_domain:
#             raise HTTPException(status_code=400, detail="Nuevo dominio no proporcionado")

#         # Buscar y actualizar el correo de todos los usuarios
#         users_collection.update_many(
#             {},
#             [{"$set": {"email": {"$concat": [{"$arrayElemAt": [{"$split": ["$email", "@"]}, 0]}, "@", new_domain]}}}]
#         )

#         return {"message": f"Todos los correos actualizados al dominio {new_domain}"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))