import binascii
from app.mensaje import Mensaje
from src.app.chat import Chat
from src.app.contacto import Contacto
import pytest
import pytest_asyncio
from unittest.mock import MagicMock, _patch_dict, patch
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives.asymmetric.padding import MGF1
from cryptography.hazmat.primitives.hashes import SHA256

# poetry run pytest test_chat.py
def test01_crearChat():
    assert Chat(00, None, None)

def test02_obtenerIdChat():
    chat= Chat(1, None, None)
    assert chat.getID_Chat()==1

def test03_ceroMiembrosAlCrearChat():
    chat = Chat(1, None, None)
    assert len(chat.getMiembros())==0

def test04_addMiembros():
    chat = Chat(1, None, None)
    #falta añadir miembros, pero como nose si tiene alias y tal
    #pregunto y lo añado
    pass

@pytest.fixture
def crear_chat() -> Chat:
    # Creamos un chat de prueba
    chat_hash = hashes.Hash(hashes.SHA256())
    chat_hash = chat_hash.finalize()
    priv_key = rsa.generate_private_key(65537, 2049)
    pub_key = priv_key.public_key()
    return Chat(chat_hash, pub_key, priv_key)

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
            Mensaje("Prueba", binascii.hexlify(chat.id_chat).decode('utf-8'), ttl=None)
        )
    
    # Verificamos que se han enviado todos los mensajes
    assert response == 2

@patch("app.sockets.ConnectionManager.get_messages")
def test_read_messages(mock_get_messages, crear_chat):
    chat = crear_chat
    chat_hash_str = binascii.hexlify(chat.id_chat).decode('utf-8')
    mensaje = Mensaje("Prueba", chat_hash_str, ttl=None)

    # Creamos un mensaje de prueba y mockeamos la respuesta del CM para que lo devuelva
    mensaje_cifrado = binascii.hexlify(
        chat.pub_key.encrypt(
            mensaje.to_json().encode('utf-8'),
            padding=OAEP(
                mgf=MGF1(SHA256()),
                algorithm=SHA256(),
                label=None
            )
        )
    ).decode('utf-8')
    mock_get_messages.return_value = [mensaje_cifrado]

    # Comprobamos que se lee el mensaje
    assert chat.read_new_messages()[0].texto == mensaje.texto

    

