from unittest.mock import patch
import pytest
#from app.gui.app import MessageApp
from app.chat import Chat
from app.mensaje import Mensaje
from cryptography.fernet import Fernet
from app.gui.app import MessageApp
from cryptography.hazmat.primitives import hashes
from app.crud import insertar_mensaje
from app.cyphersuite import cifrar_mensaje, hash_to_string
from app.file_manager import leer_usuario
from app.config_manager import ConfigManager
from app.sockets import ConnectionManager
import sqlite3 as sql
import os

TEST_DB = "resources/tests.db"

@pytest.fixture(scope="session", autouse = True)
def crear_datos_para_test():
    conn = sql.connect(TEST_DB)

    cursor = conn.cursor()
    cursor.execute("CREATE TABLE Chat(id_chat text, key text, PRIMARY KEY (id_chat))")
    cursor.execute("CREATE TABLE Mensaje(mensaje_cifrado text, PRIMARY KEY (mensaje_cifrado))")

    conn.commit()
    conn.close()

    yield
    os.remove(TEST_DB)

@pytest.fixture
def crear_chat() -> Chat:
    chat_hash = hashes.Hash(hashes.SHA256())
    chat_hash = chat_hash.finalize()
    key = Fernet.generate_key()
    return Chat(chat_hash, key)

def crear_mensaje(texto:str, chat: Chat) -> Mensaje:
    mensaje = Mensaje(texto, hash_to_string(chat.id_chat), hash_to_string(chat.id_chat), None)
    mensaje_cifrado = cifrar_mensaje(mensaje, chat.key)
    insertar_mensaje(mensaje_cifrado)
    return mensaje


@patch("app.crud.RUTA_BBDD", TEST_DB)
def test_leer_mensajes(crear_chat: Chat):
    chat = crear_chat
    
    crear_mensaje("Hola 1", chat)
    crear_mensaje("Hola 2", chat)
    
    cm = ConfigManager()
    with patch.object(cm, "user", chat):
        app = MessageApp()
        app.leer_mensajes([chat])

    # Comprobamos que los mensajes se han añadido al chat
    assert len(chat.messages) == 2

def test_cargar_configuracion_carga_user():
    app = MessageApp()
    app.cargar_configuracion()

    user = leer_usuario()

    assert ConfigManager().user.hash == user.hash

def test_cargar_configuracion_carga_cm():
    app = MessageApp()
    app.cargar_configuracion()
    cm = ConfigManager().connection_manager

    assert cm is not None and isinstance(cm, ConnectionManager)
