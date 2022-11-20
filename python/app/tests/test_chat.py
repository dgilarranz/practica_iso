import binascii
from app.mensaje import Mensaje
from app.chat import Chat
from app.contacto import Contacto
from app.config_manager import ConfigManager
from app.sockets import ConnectionManager
from app.observer import Observer
import pytest
import pytest_asyncio
import asyncio
from unittest.mock import patch
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives.asymmetric.padding import MGF1
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.fernet import Fernet

@pytest.fixture(autouse=True)
def crear_connection_manager():
    cm = ConnectionManager()
    ConfigManager().connection_manager = cm

# poetry run pytest test_chat.py
def test01_crearChat():
    assert Chat(00, None)

def test02_obtenerIdChat():
    chat= Chat(1, None)
    assert chat.getID_Chat()==1

def test03_ceroMiembrosAlCrearChat():
    chat = Chat(1, None)
    assert len(chat.getMiembros())==0

def test04_addMiembros():
    chat = Chat(1, None)
    #falta añadir miembros, pero como nose si tiene alias y tal
    #pregunto y lo añado
    pass

@pytest_asyncio.fixture
async def crear_chat() -> Chat:
    # Creamos un chat de prueba
    chat_hash = hashes.Hash(hashes.SHA256())
    chat_hash = chat_hash.finalize()
    key = Fernet.generate_key()

    # Arrancamos el servidor
    cm = ConfigManager().connection_manager
    server_task = asyncio.create_task(cm.start_service())

    yield Chat(chat_hash, key)

    # Paramos el servidor
    server_task.cancel()

@pytest.mark.asyncio
@patch("app.sockets.ConnectionManager.send_message")
async def test_send_message(mock_send_message, crear_chat):
    chat = crear_chat

    # Todos los mensajes se envían corretamente
    mock_send_message.return_value = True

    # Enviamos un mensaje de prueba a los contactos (Vacío)
    miembros = set()
    miembros.add(Contacto("clave", "1.1.1.1", "hash_c1"))
    miembros.add(Contacto("clave", "2.2.2.2", "hash_c2"))
    with patch.object(chat, 'miembros', miembros):
        response = await chat.send_message(
            Mensaje("Prueba", binascii.hexlify(chat.id_chat).decode('utf-8'), "id_user", ttl=None)
        )
    
    # Verificamos que se han enviado todos los mensajes
    assert response == 2

@patch("app.sockets.ConnectionManager.get_messages")
def test_read_messages(mock_get_messages, crear_chat):
    chat = crear_chat
    chat_hash_str = binascii.hexlify(chat.id_chat).decode('utf-8')
    mensaje = Mensaje("Prueba", chat_hash_str,"id_user", ttl=None)

    # Creamos un mensaje de prueba y mockeamos la respuesta del CM para que lo devuelva
    mensaje_cifrado = Fernet(chat.key).encrypt(mensaje.to_json().encode("utf-8")).decode('utf-8')
    mock_get_messages.return_value = [mensaje_cifrado]

    # Comprobamos que se lee el mensaje
    assert chat.read_new_messages()[0].texto == mensaje.texto

def test_chat_is_instance_of_observer():
    assert isinstance(Chat("id", b"key"), Observer)

def test_chat_is_subscribed_to_connection_manager():
    cm = ConfigManager().connection_manager
    chat = Chat("id", b"key")

    assert chat in cm.subscribers

def test_chat_checks_chats_on_update(crear_chat: Chat):
    cm = ConfigManager().connection_manager
    chat = crear_chat

    with patch.object(chat, "read_new_messages") as mock_read_messages:
        cm.notify()
        mock_read_messages.assert_called_once()