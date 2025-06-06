"""
nomia_utils.py

Este módulo contiene utilidades de uso general para el desarrollo de aplicaciones. Proporciona funciones relacionadas con la manipulación 
de fechas, generación de códigos aleatorios, limpieza y transformación de cadenas de texto, entre otros.

Funciones principales:
- **Fechas y horas**: 
  - Obtener nombres de meses en diferentes idiomas (`get_name_meses`).
  - Formatear fechas y horas actuales (`get_current_date_str`, `get_current_time_str`).
  - Convertir fechas entre formatos (`get_date_from_iso_date`, `string_date_to_date`, etc.).
  - Generar timestamps para logs (`get_time_stamp`).

- **Manipulación de texto**:
  - Limpiar cadenas de caracteres (`remove_html`, `clean`, `clean_hard`).
  - Escapar caracteres para evitar errores (`escape`).
  - Convertir formatos de fechas en cadenas (`string_date_to_param_date`, `param_date_to_string_date`).

- **Generación aleatoria**:
  - Crear códigos aleatorios basados en un conjunto configurable de caracteres (`random_code`).

Este archivo está diseñado para ser modular y reutilizable, facilitando tareas comunes que se presentan en el desarrollo de software. 
Las funciones relacionadas con fechas son especialmente útiles para trabajar con formatos internacionales y manipular datos de bases 
de datos como MongoDB.
"""
from datetime import datetime
import re
import random
import string
import os 

def debug_log(message: str):
    """Muestra el mensaje en el log SOLO EN DEVELOPMENT"""
    environment = os.getenv("ENVIRONMENT", "deve").lower()
    if environment == "development":
        print(f"[DEBUG] {message}")

# Devuelve un array con los nombres de los meses
def get_name_meses(lang: str):
    if lang == 'es':
        return ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    elif lang == 'en':
        return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    else:
        return ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

# Devuelve Fecha Actual con formato dd/mm/aaaa
def get_current_date_str(lang: str) -> str:
    f = datetime.now()
    if lang == 'en':
        return f.strftime('%m/%d/%Y')
    else:
        return f.strftime('%d/%m/%Y')

# Devuelve Hora Actual con formato hh:mm:ss
def get_current_time_str() -> str:
    return datetime.now().strftime('%H:%M:%S')

# Convierte una fecha tipo datetime en cadena con formato dd/mm/aaaa hh:mm:ss
def get_date_time_string(date: datetime, lang: str = 'es') -> str:
    if lang == 'en':
        return date.strftime('%m/%d/%Y %H:%M')
    else:
        return date.strftime('%d/%m/%Y %H:%M')

# Convierte una fecha tipo datetime en cadena con formato dd/mm/aaaa
def get_date_string(date: datetime, lang: str) -> str:
    if lang == 'en':
        return date.strftime('%m/%d/%Y')
    else:
        return date.strftime('%d/%m/%Y')

# Devuelve la fecha y la hora concatenadas para logs
def get_time_stamp() -> str:
    return f"[{get_current_date_str('es')}, {get_current_time_str()}]"

# Devuelve la fecha en formato dd/mm/aaaa desde una fecha ISO (MongoDB)
def get_date_from_iso_date(iso_str: str, lang: str) -> str:
    date_obj = datetime.fromisoformat(iso_str)
    return get_date_string(date_obj, lang)

# Devuelve la hora en formato hh:mm:ss desde una fecha ISO (MongoDB)
def get_time_from_iso_date(iso_str: str) -> str:
    date_obj = datetime.fromisoformat(iso_str)
    return date_obj.strftime('%H:%M:%S')

# Devuelve la hora en formato hh:mm desde una fecha ISO (MongoDB)
def get_short_time_from_iso_date(iso_str: str) -> str:
    date_obj = datetime.fromisoformat(iso_str)
    return date_obj.strftime('%H:%M')

# Convierte una fecha en formato datetime a ISO string
def date_to_iso_date(date: datetime) -> str:
    return date.isoformat()

# Convierte un string de fecha en formato dd/mm/yyyy,hh:mm:ss a datetime
def string_date_to_date(date_str: str) -> datetime:
    date_str = re.sub(r'[,\s:-]', '/', date_str)
    elems = list(map(int, date_str.split('/')))
    while len(elems) < 6:
        elems.append(0)
    return datetime(elems[2], elems[1], elems[0], elems[3], elems[4], elems[5])

# Igual que el anterior pero redondea los segundos a 0
def string_date_to_date_0_sec(date_str: str) -> datetime:
    date_str = re.sub(r'[,\s:-]', '/', date_str)
    elems = list(map(int, date_str.split('/')))
    while len(elems) < 6:
        elems.append(0)
    return datetime(elems[2], elems[1], elems[0], elems[3], elems[4], 0)

# Convierte una fecha en formato string dd/mm/yyyy,hh:mm:ss a formato dd-mm-yyyy,hh-mm-ss
def string_date_to_param_date(date_str: str) -> str:
    return date_str.replace('/', '-')

# Convierte una fecha en formato dd-mm-yyyy,hh:mm:ss a formato string dd/mm/yyyy,hh:mm:ss
def param_date_to_string_date(date_str: str) -> str:
    return date_str.replace('-', '/')

# Genera un código aleatorio basado en un conjunto de caracteres
def random_code(max_length: int = 12, char_set: str = string.ascii_letters + string.digits) -> str:
    return ''.join(random.choice(char_set) for _ in range(max_length))

# Elimina etiquetas HTML de una cadena
def remove_html(text: str) -> str:
    return re.sub(r'<[^>]*>', '', text)

# Escapa una cadena de texto
def escape(text: str) -> str:
    return text.replace("'", "\\'").replace('"', '\\"').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# Elimina caracteres especiales de una cadena
def clean(text: str) -> str:
    return remove_html(text).translate(str.maketrans('', '', r'`ª´·¨Ç~¿!#$%^&*()_|+=?;\'",<>[]{}\\'))

# Elimina caracteres especiales, incluyendo espacios
def clean_hard(text: str) -> str:
    return clean(text).replace(' ', '')
