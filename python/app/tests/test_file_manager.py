import binascii
from app.setup import inicializar_usuario
from app.file_manager import guardar_usuario
from app.file_manager import leer_usuario
import json
import pytest
import os
from unittest.mock import patch

def test_guardar_usuario():
    usuario = inicializar_usuario()
    guardar_usuario(usuario) 
    f = open('resources/config.json', 'r') #abre un fichero en modo lectura
    contenido = json.load(f)
    assert contenido['hash'] == binascii.hexlify(usuario.hash).decode('UTF-8')

@pytest.fixture
def usuario_prueba():
    # Creamos un usuario de prueba y lo guardamos en el fichero
    user = inicializar_usuario()

    # Devolvemos el usuario y esperamos a que finalice el test
    yield user

    # Borramos el fichero de prueba
    os.remove("resources/fichero_prueba_config.json")


@patch("app.file_manager.FICHERO_CONFIG", "resources/fichero_prueba_config.json")
def test_leer_usuario(usuario_prueba):
    # Guardamos el usuario de prueba en el fichero
    guardar_usuario(usuario_prueba)

    # Leemos el fichero y verificamos los campos
    usuario_leido = leer_usuario()

    assert usuario_leido.hash == usuario_prueba.hash