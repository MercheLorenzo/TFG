"""
db.py - Configuración y manejo de la conexión asíncrona a MongoDB.

Este archivo establece la conexión a la base de datos MongoDB utilizando Motor, 
un cliente asíncrono de MongoDB para Python. La URI y el nombre de la base 
de datos se gestionan a través de las configuraciones definidas en el archivo 
config.py. Este archivo también contiene una función para cerrar la conexión 
a la base de datos.

La conexión y la interacción con las colecciones específicas (por ejemplo, 
usuarios, clientes, empresas) deben definirse en los modelos correspondientes 
y no en este archivo.

Funciones:
- close_db: Cierra la conexión a la base de datos MongoDB.
"""
from motor.motor_asyncio import AsyncIOMotorClient
import json
import os
from src.Config.config import config

# Configurar la conexión a MongoDB usando las variables de configuración
MONGODB_URI = config.DB  # Usar la URI de la BD desde config.py
DATABASE_NAME = config.DB_NAME  # Extraer el nombre de la BD de la URI

client = AsyncIOMotorClient(MONGODB_URI)
db = client[DATABASE_NAME]
# LA DEFINICION DE LA BD DE CADA MODELO (users, clients, companies...) VA EN SU MODELO CORRESPONDIENTE
# ASI COMO LA INICIALIZACION DE SU BD/COLECCION CORRESPONDIENTE, y las funcionalidades adicionales que quieras añadir (add, update, get info...)

# Cierra la conexión al terminar
def close_db():
    client.close()  # Cierra la conexión al terminar
