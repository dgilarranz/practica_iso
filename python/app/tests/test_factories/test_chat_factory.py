from app.chat import Chat
from app.crud import leer_chat
from app.cyphersuite import hash_to_string
from app.factories.chat_factory import ChatFactory, ChatExistsException
import pytest
from unittest.mock import patch
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
import sqlite3 as sql
import os

@pytest.fixture(scope="session", autouse = True)
def crear_base_datos_para_tests():
    conn = sql.connect("resources/test_database.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE Chat(id_chat text, key text, PRIMARY KEY (id_chat))")
    conn.commit()
    conn.close()
    yield
    os.remove("resources/test_database.db")


@patch("app.crud.RUTA_BBDD", "resources/test_database.db")
def test_creation_of_new_chat_not_in_database():
    chat = ChatFactory().create_chat()
    id_chat = hash_to_string(chat.id_chat)
    db_chat = leer_chat(id_chat)
    assert chat.id_chat == db_chat.id_chat

@patch("app.crud.RUTA_BBDD", "resources/test_database.db")
def test_another_creation_of_new_chat_not_in_database():
    chat = ChatFactory().create_chat()
    id_chat = hash_to_string(chat.id_chat)
    db_chat = leer_chat(id_chat)
    assert chat is not None and db_chat is not None and chat.id_chat == db_chat.id_chat

@patch("app.crud.RUTA_BBDD", "resources/test_database.db")
def test_chats_have_different_ids():
    factory = ChatFactory()
    chat_1 = factory.create_chat()
    chat_2 = factory.create_chat()
    assert chat_1.id_chat != chat_2.id_chat

@patch("app.crud.RUTA_BBDD", "resources/test_database.db")
def test_create_new_chat_with_known_params():
    key = Fernet.generate_key()

    chat_hash = hashes.Hash(hashes.SHA256())
    chat_hash.update(key)
    chat_hash = chat_hash.finalize()

    str_key = hash_to_string(key)
    str_hash = hash_to_string(chat_hash)

    chat = ChatFactory().create_chat(str_hash, str_key)
    db_chat = leer_chat(hash_to_string(chat.id_chat))

    assert chat.id_chat == db_chat.id_chat
