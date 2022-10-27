from unittest.mock import patch
import pytest
from app.gui.app import MessageApp
from app.chat import Chat
from app.mensaje import Mensaje
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes

@pytest.fixture
def crear_chat():
    chat_hash = hashes.Hash(hashes.SHA256())
    chat_hash = chat_hash.finalize()
    key = Fernet.generate_key
    return Chat(chat_hash, key)

def crear_mensaje(texto:str, chat: Chat):
    return Mensaje(texto, chat.id_chat, "sender prueba")

@patch("app.crud.leer_mensajes")
def test_leer_mensajes(mock_leer_mensajes, crear_chat: Chat):
    chat = crear_chat
    mensajes = [
        crear_mensaje("Hola 1", chat),
        crear_mensaje("Hola 2", chat)
    ]
    mock_leer_mensajes.return_value = mensajes

    app = MessageApp()

    # Asociamos los mensajes
    app.leer_mensajes([chat])

    # Comprobamos que los mensajes se han añadido al chat
    added = True
    for msg in mensajes:
        added = added and (msg in chat)
    
    assert added

