"""
enum.py

Este archivo define las enumeraciones utilizadas en los servicios de Santra.

Enumeraciones:
- ErrorCategory: Categorías de error para clasificar los mensajes de error (ERROR, WARNING, INFO).
- MessageType: Tipos de mensajes que pueden ser enviados (OK, INFO, QUESTION).

Estas enumeraciones facilitan la gestión de diferentes tipos de mensajes y errores en el sistema.
"""
from enum import Enum

class ErrorCategory(Enum):
    ERROR = 0
    WARNING = 1
    INFO = 2

class MessageType(Enum):
    OK = 0
    INFO = 1
    QUESTION = 2
