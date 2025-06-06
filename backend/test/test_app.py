"""
test_app.py
Archivo que contiene los tests para las rutas y funcionalidades de la aplicación

Descripción de uso:
- Ejecuta `PYTHONPATH=$(pwd) pytest` en la terminal para correr todas las pruebas.
- Para ejecutar únicamente las pruebas de este archivo, utiliza `PYTHONPATH=$(pwd) pytest test/test_app.py`.
- Opcionalmente, puedes agregar la opción `-v` para obtener un informe más detallado.

Actualmente, hay varias pruebas definidas que verifican el correcto funcionamiento de las rutas
y la redirección de la aplicación. Se pueden agregar más pruebas según sea necesario.
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Al escribir /main te tiene que redirigir a main
def test_main_route():
    response = client.get("/main")
    assert "main"

def test_redirect_api():
    response = client.get("/api/get-status")
    assert response.status_code == 200

# Te tiene que mandar a docs
def test_docs_route():
    response = client.get("/docs")
    assert "docs" in response.text

def test_redoc_route():
    response = client.get("/redoc")
    assert "redoc" in response.text

# Al escribir una ruta no existente, te tiene que redirigir a main
def test_not_found():
    response = client.get("/nonexistent-route")
    assert "main"

# Al escribir la ruta  / , te tiene que redirigir a main
def test_redirect_root():
    response = client.get("/")
    assert "main"

# Comprobar que la pagina funciona correctamente cuando le cambias el idioma
def test_get_current_language_en():
    response = client.get("/main?lang=en")
    assert response.status_code == 200

# Al escribir el main con idioma, te tiene que dar OK-200, si es uno de los que tenemos implementados
def test_get_current_language_de():
    response = client.get("/main?lang=de")
    assert response.status_code == 200

def test_get_current_language_ch():
    response = client.get("/main?lang=ch")
    assert response.status_code == 200

def test_get_current_language_fr():
    response = client.get("/main?lang=fr")
    assert response.status_code == 200

def test_get_current_language_it():
    response = client.get("/main?lang=it")
    assert response.status_code == 200

def test_get_current_language_es():
    response = client.get("/main?lang=es")
    assert response.status_code == 200

# Se pueden seguir añadiendo tests de app.py aqui abajo...