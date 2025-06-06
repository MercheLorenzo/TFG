"""
types.py

Este archivo contiene definiciones de tipos utilizados en los servicios de Santra.

Tipos:
- RoutesInput: Define el tipo para la entrada relacionada con las rutas de la aplicación (con una clave 'app' de tipo genérico).
- DBInput: Define el tipo para la entrada relacionada con la base de datos (con una clave 'db' que especifica el nombre de la base de datos como una cadena).

Estos tipos mejoran la legibilidad y la comprobación de tipos en el código, facilitando el desarrollo y mantenimiento.
"""

from typing import TypedDict

class RoutesInput(TypedDict):
    app: any 

class DBInput(TypedDict):
    db: str
