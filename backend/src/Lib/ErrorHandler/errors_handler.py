"""
errors_handler.py

Módulo para la gestión de errores con soporte para categorías de error: ERROR, WARNING, INFO.
Utiliza Pydantic para definir modelos de error y Enum para categorizar los errores.
Proporciona un sistema de logging configurable, permitiendo ajustar el nivel de detalles de los logs (INFO, DEBUG, WARNING, ERROR, CRITICAL).
Define errores comunes con códigos y mensajes predefinidos para facilitar su manejo y seguimiento.
La clase 'ErrorHandler' maneja los errores, permite imprimir los mensajes con un formato estructurado y obtener la información del error en formato diccionario.
"""
from pydantic import BaseModel
from enum import Enum
import datetime
import logging

# Configuración del logger (puedes ajustar el nivel)
# Puedo cambiar el nivel: 
# CRITICAL solo muestra los errores mas graves, ERROR errores importantes, 
# WARNING advertencias sobre posibles problemas, INFO informacion general sobre el funcionamiento del servidor (valor por defecto)
# DEBUG informacion detallada de depuracion
logger = logging.getLogger("errors_handler")
logging.basicConfig(level=logging.INFO)

# Enumeración para las categorías de error
class ErrorCategory(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"

# Definición de errores
ERRORS = {
    "DEMO_ERROR": {"code": "ERR_000", "message": "Demo Error", "category": ErrorCategory.ERROR},
    "UNHANDLED_EXCEPTION": {"code": "ERR_001", "message": "Unhandled Exception", "category": ErrorCategory.ERROR},
    "SERVER_CICLE_BLOCK": {"code": "ERR_002", "message": "Server cicle took more time than maximum allowed:", "category": ErrorCategory.WARNING},
    "SERVER_ROUTE_ERROR": {"code": "ERR_003", "message": "The requested route is not available", "category": ErrorCategory.ERROR},
    "DB_CONNECTION_ERROR": {"code": "ERR_004", "message": "Error connecting to database", "category": ErrorCategory.ERROR},
    "DB_DISCONNECTION_ERROR": {"code": "ERR_005", "message": "Service Disconnected from Database", "category": ErrorCategory.ERROR},
    "DB_CREATE_ERROR": {"code": "ERR_006", "message": "Error saving register to database", "category": ErrorCategory.ERROR},
    "REQUEST_PARAMS_ERROR": {"code": "ERR_007", "message": "Error in request parameters", "category": ErrorCategory.ERROR},
    "VALIDATION_ERROR": {"code": "ERR_008", "message": "Error validating request parameters", "category": ErrorCategory.ERROR},
    "READ_WRITE_DB_ERROR": {"code": "ERR_009", "message": "Error reading or writing from/to database", "category": ErrorCategory.ERROR}
}

# Clase de modelo de error utilizando Pydantic
class ErrorModel(BaseModel):
    code: str
    message: str
    category: ErrorCategory
    module: str = ""
    trace: str = ""

# Clase para la gestión de errores
class ErrorHandler:
    def __init__(self, error: ErrorModel, module: str, trace: str = ""):
        self._code = error.code
        self._message = error.message
        self._category = error.category
        self._module = module
        self._trace = trace

    @property
    def code(self) -> str:
        return self._code

    @property
    def message(self) -> str:
        return self._message

    @property
    def category(self) -> ErrorCategory:
        return self._category

    @property
    def module(self) -> str:
        return self._module

    @property
    def trace(self) -> str:
        return self._trace or ""

    def print_error(self) -> None:
        category_display = {
            ErrorCategory.ERROR: "[ ERROR ]",
            ErrorCategory.WARNING: "[ WARNING ]",
            ErrorCategory.INFO: "[ INFO ]"
        }
        print_category = category_display.get(self._category, "[ ERROR ]")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print_line = f"{timestamp} {print_category} <{self._module}> {self._code} - {self._message}"
        if self._trace:
            print_line += f"\nTrace: {self._trace}"
        logger.error(print_line)

    def get_error_object(self) -> dict:
        return {
            "code": self._code,
            "message": self._message,
            "category": self._category.value,
            "module": self._module,
            "addInfo": self._trace
        }
