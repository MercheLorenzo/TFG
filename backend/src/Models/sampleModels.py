"""
sampleModels.py

Este archivo define los modelos de datos utilizando Pydantic para manejar las solicitudes relacionadas con tokens en la API.

- TokenRequest: Modelo para recibir el nombre de usuario en las solicitudes de creación de token.
- VerifyTokenRequest: Modelo para recibir y verificar el token en las solicitudes de validación de token.

Ambos modelos son utilizados para asegurar la validación y estructura de los datos en las funcionalidades de creación y verificación de tokens.
"""
from pydantic import BaseModel

# Modelos pydantic para usar luego sobre las funcionalidades de crear y verificar tokens

class TokenRequest(BaseModel):
    username: str

class VerifyTokenRequest(BaseModel):
    token: str
