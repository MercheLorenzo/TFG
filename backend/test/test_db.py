"""
test_bd.py
Archivo que contiene los tests para la base de datos de la aplicación

Descripción de uso:
- Ejecuta `PYTHONPATH=$(pwd) pytest` en la terminal para correr todos los tests.
- Para ejecutar únicamente las pruebas de este archivo, utiliza `PYTHONPATH=$(pwd) pytest test/test_db.py`.
- Opcionalmente, puedes agregar la opción `-v` para un modo detallado.

Actualmente, hay un conjunto básico de pruebas definidas, pero se pueden agregar más para 
asegurar el correcto funcionamiento de las operaciones relacionadas con la base de datos.
"""
import sys
import os
import pytest
from src.Models.userModel import db, initialize_users_db, users_collection
from src.db import close_db
import json
import asyncio

# Carga de datos desde el archivo JSON para el test
TEST_DATA_FILE = 'test/users.json'

@pytest.fixture(scope="module")
def event_loop():
    """Define un event loop para los tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
    
# Prueba que se inicializa correctamente la BD de usuarios, que es la unica implementada de momento
@pytest.mark.asyncio
async def test_initialize_db():
    await initialize_users_db()
    # Asegúrate de que la colección esté vacía al inicio
    assert await db.users_collection.count_documents({}) == 0

@pytest.mark.asyncio
async def test_add_users_from_file():
    # Asegúrate de que el archivo existe
    assert os.path.exists(TEST_DATA_FILE), f"El archivo {TEST_DATA_FILE} no existe."

    # Carga los usuarios del archivo JSON
    with open(TEST_DATA_FILE, 'r') as file:
        users_data = json.load(file)
        assert isinstance(users_data, list), "El archivo JSON debe contener una lista de usuarios."

    # Itera sobre los usuarios y agrégalos si no existen
    for user in users_data:
        email = user.get("email")
        assert email, "Cada usuario debe tener un campo 'email'."

        # Comprueba si el email ya existe en la base de datos
        existing_user = await users_collection.find_one({"email": email})
        if not existing_user:
            try:
                # Inserta el usuario si no existe
                await users_collection.insert_one(user)
                print(f"Usuario con email {email} añadido.")
            except DuplicateKeyError:
                print(f"Usuario con email {email} ya existe (clave duplicada).")
        else:
            print(f"Usuario con email {email} ya existe en la base de datos.")
    
    # Verifica que la colección contiene los usuarios esperados
    db_emails = [user["email"] async for user in users_collection.find({}, {"email": 1, "_id": 0})]
    for user in users_data:
        assert user["email"] in db_emails, f"El usuario con email {user['email']} no se añadió correctamente."

# Prueba de cierre de la BD
@pytest.mark.asyncio
async def test_close_db():
    close_db()  # Asegúrate de que se cierra la conexión
    # Aquí puedes verificar que la conexión se haya cerrado si es necesario

# Se pueden añadir mas tests aqui abajo...