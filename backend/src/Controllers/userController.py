"""
userController.py

Este archivo actúa como controlador principal para gestionar las operaciones CRUD relacionadas con la entidad `User`.  
Se encarga de interactuar con la colección `users_collection` en MongoDB, implementando validaciones y gestión de errores HTTP.

**Resumen de Funcionalidades**:
1. **`create_user`** (POST):
   - Crea un nuevo usuario en la base de datos.
   - Verifica si el correo electrónico ya existe para evitar duplicados.

2. **`get_user_by_email`** (GET):
   - Busca y devuelve un usuario usando su correo electrónico.
   - Maneja errores si el usuario no existe.

3. **`count_users`** (GET):
   - Cuenta el número total de usuarios en la base de datos y devuelve el resultado.

4. **`search_users`** (GET):
   - Permite buscar usuarios parcialmente por nombre o apellidos, utilizando expresiones regulares para coincidencias flexibles.
   - Devuelve resultados formateados (ID y campos clave).

**Características Adicionales Comentadas**:
- **Eliminar Usuario (`delete_user`)**:
  - Elimina un usuario específico basado en su ID.
- **Actualizar Usuario (`update_user`)**:
  - Actualiza campos de un usuario específico.
- **Actualizar dominio de correos electrónicos**:
  - Permite actualizar el dominio de todos los correos en la base de datos mediante una única operación.

**Responsabilidad Principal**:
Este módulo actúa como la lógica intermedia entre la base de datos y la capa de rutas/solicitudes en la API.  
Se encarga de:
- **Validaciones** de datos.
- Gestión de **errores HTTP**.
- Procesamiento de datos desde MongoDB para adaptarlos a las respuestas de la API.

**Uso Práctico**:
Sirve como plantilla para construir endpoints robustos y escalables para operaciones relacionadas con la gestión de usuarios.
"""
from fastapi import HTTPException
from pydantic import EmailStr
from bson import ObjectId
from src.Models.userModel import users_collection
from typing import List, Optional
from src.Content.i18n import load_dictionary
from src.Models.userModel import User, UserUpdate, UpdateEmailDomain
from datetime import datetime

# Código de color ANSI
RED     = "\033[31m"
GREEN   = "\033[32m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"
RESET   = "\033[0m"
current_time = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')  # Formato de fecha y hora

async def check_database_connection_users():
    """Prueba la conexión a la base de datos al arrancar o para verificar problemas."""
    try:
        # Ejecuta una operación básica como `ping` o cuenta documentos
        await users_collection.database.command("ping")
        print(f"{GREEN}|santra-c | {WHITE}[{current_time}] [ {GREEN}OK{RESET} ] Successfully connected to users database.")
        return True
    except Exception as e:
        print(f"{GREEN}|santra-c | {WHITE}[{current_time}] [ {RED}ERROR{RESET} ] Couldn't connect to users database.")
        # raise HTTPException(status_code=500, detail="Error de conexión con la base de datos de usuarios")

# Crear un usuario en la base de datos (POST)
async def create_user(user: User):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=409, detail="El usuario con este correo ya existe")

    try:
        new_user = user.dict()
        result = await users_collection.insert_one(new_user)

        new_user["_id"] = str(result.inserted_id)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear el usuario: " + str(e))

# Buscar un usuario por su correo electrónico (GET)
async def get_user_by_email(email: str):
    try:
        user = await users_collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        user["_id"] = str(user["_id"])
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Contar el número total de usuarios en la base de datos (GET)
async def count_users():
    try:
        count = await users_collection.count_documents({})
        return {'total_users': count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Buscar usuarios por nombre o apellido parcial (GET)
async def search_users(name: str):
    try:
        cursor = users_collection.find({
            "$or": [
                {"firstName": {"$regex": name, "$options": "i"}},
                {"lastName": {"$regex": name, "$options": "i"}},
                {"secondLastName": {"$regex": name, "$options": "i"}}
            ]
        }, {'_id': 1, 'email': 1, 'firstName': 1, 'lastName': 1, 'secondLastName': 1})

        users = await cursor.to_list(length=None)

        if not users:
            raise HTTPException(status_code=404, detail="No users found")

        for user in users:
            user['_id'] = str(user['_id'])

        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# # Eliminar un usuario de la base de datos (DELETE)
# async def delete_user(user_id: str):
#     try:
#         obj_id = ObjectId(user_id)
#         user = await users_collection.find_one({"_id": obj_id})
#         if not user:
#             raise HTTPException(status_code=404, detail="Usuario no encontrado")
#         await users_collection.delete_one({"_id": obj_id})
#         return {"message": f'Usuario con ID {user_id} eliminado exitosamente'}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Actualizar un usuario existente en la base de datos (PUT)
# async def update_user(user_id: str, user: UserUpdate):
#     try:
#         obj_id = ObjectId(user_id)
#         updated_data = {k: v for k, v in user.dict().items() if v is not None}
#         if not updated_data:
#             raise HTTPException(status_code=400, detail="No hay datos para actualizar")

#         existing_user = await users_collection.find_one({"_id": obj_id})
#         if not existing_user:
#             raise HTTPException(status_code=404, detail="Usuario no encontrado")

#         await users_collection.update_one({"_id": obj_id}, {"$set": updated_data})
#         updated_user = await users_collection.find_one({"_id": obj_id})
#         updated_user["_id"] = str(updated_user["_id"])

#         return updated_user
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Actualizar el dominio del correo de todos los usuarios (PUT)
# async def update_email_domain(domain: UpdateEmailDomain):
#     try:
#         new_domain = domain.new_domain
#         if not new_domain:
#             raise HTTPException(status_code=400, detail="Nuevo dominio no proporcionado")

#         users_collection.update_many(
#             {},
#             [{"$set": {"email": {"$concat": [{"$arrayElemAt": [{"$split": ["$email", "@"]}, 0]}, "@", new_domain]}}}]
#         )
#         return {"message": f"Todos los correos actualizados al dominio {new_domain}"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
