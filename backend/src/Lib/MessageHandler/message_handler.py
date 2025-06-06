"""
message_handler.py

Módulo para la gestión y visualización de mensajes de log.

Utiliza colores para diferenciar tipos de mensajes: OK, INFO, QUESTION.
Define un formato estándar de log con fecha, tipo de mensaje y contenido.
Los mensajes se formatean y muestran por consola con diferentes estilos de color.
Incluye la clase 'Message' para crear y manejar mensajes, y 'MessageType' para los tipos de mensaje.
Los mensajes pueden ser dinámicos, con parámetros que se insertan en el texto.
"""
from colorama import Fore, Style
from datetime import datetime

# Definición de tipos de mensajes
class MessageType:
    OK = 0
    INFO = 1
    QUESTION = 2

# Definición de mensajes de log
MESSAGES = {
    "DEMO_MESSAGE": "This is a Demo Message",
    "SANTRA_SERVICE_STARTED": "Santra Service Started at Port {} - Env: {}",
    "SECRET_VAULT_TEST": "Secret Vault Test: {}",
    "DB_CONNECTION_SUCCESS": "Successfully connected to database"
}

class Message:
    def __init__(self, message: str, message_type: int = MessageType.INFO, params: list = None):
        self._message = message
        self._type = message_type
        self._params = params or []

    @property
    def message(self):
        return self._message.format(*self._params)

    @property
    def type(self):
        return self._type

    @property
    def params(self):
        return self._params

    @message.setter
    def message(self, message: str):
        self._message = message

    @type.setter
    def type(self, message_type: int):
        self._type = message_type

    @params.setter
    def params(self, params: list):
        self._params = params

    def print_message(self):
        # Mapeo de tipo de mensaje a estilos de color
        if self._type == MessageType.OK:
            print_type = f"[ {Fore.GREEN + Style.BRIGHT}OK{Style.RESET_ALL} ]"
        elif self._type == MessageType.INFO:
            print_type = f"[ {Fore.BLUE + Style.BRIGHT}INFO{Style.RESET_ALL} ]"
        elif self._type == MessageType.QUESTION:
            print_type = f"[ {Fore.CYAN + Style.BRIGHT}?{Style.RESET_ALL} ]"
        else:
            print_type = f"[ {Fore.BLUE + Style.BRIGHT}INFO{Style.RESET_ALL} ]"

        # Generar e imprimir la línea de log
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print_line = f"{timestamp} {print_type} {self.message}"
        print(print_line)

    def get_message_object(self):
        return {
            "message": self.message,
            "type": self.type,
            "params": self.params
        }

    @staticmethod
    def get_type_string(category: int) -> str:
        mapping = {
            MessageType.OK: "OK",
            MessageType.INFO: "INFO",
            MessageType.QUESTION: "QUESTION"
        }
        return mapping.get(category, "UNKNOWN")