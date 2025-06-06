"""
i18n.py

Este archivo proporciona las funcionalidades necesarias para la internacionalización (i18n) de la aplicación:
- Permite cargar diccionarios de traducción desde archivos JSON según el idioma solicitado.
- Si el idioma solicitado no está soportado, carga el idioma predeterminado (español).
- Implementa la obtención del idioma actual desde la URL utilizando el parámetro `?lang=<idioma>`.
- Aprovecha configuraciones globales definidas en `config.py` para los idiomas soportados y el idioma por defecto.

Este módulo es esencial para adaptar la aplicación a múltiples idiomas, mejorando la experiencia del usuario internacional.
"""
import os
import json
from fastapi import Request, Depends, HTTPException
from src.Config.config import config

# Usar las variables de configuración
SUPPORTED_LANGUAGES = config.SUPPORTED_LANGUAGES  
DEFAULT_LANGUAGE = config.DEFAULT_LANGUAGE
CONTENT_DIR = os.path.dirname(__file__)

# Cargar el diccionario en funcion del idioma seleccionado
def load_dictionary(language: str):
    """
    Carga el diccionario de traducciones en función del lenguaje pasado como parámetro.
    Si el archivo no existe, se carga el diccionario por defecto (español).
    """
    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE

    try:
        with open(os.path.join(CONTENT_DIR, f'{language}.json'), encoding='utf-8') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        with open(os.path.join(CONTENT_DIR, f'{DEFAULT_LANGUAGE}.json'), encoding='utf-8') as json_file:
            return json.load(json_file)

# Obtiene el idioma a partir del parametro de la URL
async def get_current_language(request: Request):
    """
    Obtiene el idioma actual a partir de los parámetros en la URL (?lang=<idioma>).
    Lanza un error 400 si el idioma no está en la lista de idiomas soportados.
    """
    language = request.query_params.get('lang', DEFAULT_LANGUAGE)
    if language in SUPPORTED_LANGUAGES:
        return language
    else:
        raise HTTPException(status_code=400, detail="Unsupported language")
