from unittest.mock import patch
import pytest
#from app.gui.app import MessageApp
from app.chat import Chat
from app.mensaje import Mensaje
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes

########################### ¡¡¡¡¡¡¡¡¡¡¡GUARRADA!!!!!!!!!!!! #############################
# Por incompatibilidades en los frameworks, para ejecutar los tests incluiremos en esta
# sección los métodos que estamos comprobando.
from app.crud import leer_mensaje

def leer_mensajes(chats: list[Chat]):
    mensajes = [
        crear_mensaje("Hola 1", chats[0]),
        crear_mensaje("Hola 2", chats[0])
    ]

    # Ordenamos los mensajes por tienpo
    mensajes = sorted(mensajes, key=lambda msg: msg.timestamp)
    for msg in mensajes:
        chat = list(filter(lambda chat: chat.id_chat == msg.id_chat, chats))[0]
        chat.messages.append(msg)


#########################################################################################


@pytest.fixture
def crear_chat() -> Chat:
    chat_hash = hashes.Hash(hashes.SHA256())
    chat_hash = chat_hash.finalize()
    key = Fernet.generate_key
    return Chat(chat_hash, key)

def crear_mensaje(texto:str, chat: Chat) -> Mensaje:
    return Mensaje(texto, chat.id_chat, "sender prueba")

def test_leer_mensajes(crear_chat: Chat):
    chat = crear_chat

    mensajes = [
        crear_mensaje("Hola 1", chat),
        crear_mensaje("Hola 2", chat)
    ]

    # Asociamos los mensajes
    leer_mensajes([chat])

    # Comprobamos que los mensajes se han añadido al chat
    assert len(chat.messages) == 2

