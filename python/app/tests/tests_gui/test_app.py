from unittest.mock import patch
import pytest
from app.chat import Chat
from app.factories.chat_factory import ChatFactory
from app.mensaje import Mensaje
from cryptography.fernet import Fernet
from app.gui.app import MessageApp
from cryptography.hazmat.primitives import hashes
from app.crud import insertar_mensaje, leer_mensaje
from app.cyphersuite import cifrar_mensaje, hash_to_string
from app.file_manager import leer_usuario
from app.config_manager import ConfigManager
from app.sockets import ConnectionManager
import sqlite3 as sql
from app.file_manager import leer_usuario
from app.contrato import Contrato
import os
from app.setup import cifrar_ip
from app.file_manager import leer_usuario

TEST_DB = "resources/tests.db"

@pytest.fixture(scope="function", autouse = True)
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
    ConfigManager().connection_manager = ConnectionManager()
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

@patch("asyncio.create_task")
def test_cargar_configuracion_carga_user(mock_create_task):
    app = MessageApp()
    app.cargar_configuracion()

    user = leer_usuario()

    assert ConfigManager().user.hash == user.hash

@patch("asyncio.create_task")
def test_cargar_configuracion_carga_cm(mock_create_task):
    app = MessageApp()
    app.cargar_configuracion()
    cm = ConfigManager().connection_manager

    assert cm is not None and isinstance(cm, ConnectionManager)

@patch("toga.App.add_background_task")
def test_servidor_arranca(mock_create_task):
    app = MessageApp()
    app.cargar_configuracion()

    mock_create_task.assert_called_once()

@patch("app.crud.RUTA_BBDD", TEST_DB)
def no_test_leer_mensajes_borra_mensajes_si_chat_ya_no_existe():    
    app = MessageApp()
    ConfigManager().user = leer_usuario()

    chat = ChatFactory().create_new_chat()
    mensaje = Mensaje("Mensaje de chat borrado", hash_to_string(chat.id_chat), "Fantasmita")
    mensaje_cifrado = cifrar_mensaje(mensaje, ConfigManager().user.key)
    insertar_mensaje(mensaje_cifrado)

    with pytest.raises(TypeError):
        app.leer_mensajes([])

@patch("app.setup.obtener_ip_privada")
def test_ip_subida_a_blochain(mock_obtener_ip_privada):
    ip = "1.1.1.1"

    ConfigManager().contrato = Contrato()
    mock_obtener_ip_privada.return_value = ip
    user = leer_usuario()

    with patch.object(ConfigManager().contrato, "actualizar_ip") as mock_actualizar_ip:
        app = MessageApp()
        app.inicializar_blockchain()
        ip_cifrada = cifrar_ip(user, ip)
        mock_actualizar_ip.assert_called_once()

def test_contrato_annadido_a_config_manager():
    app = MessageApp()
    app.startup()
    assert ConfigManager().contrato is not None