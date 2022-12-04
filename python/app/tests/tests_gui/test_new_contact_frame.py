import pytest
from unittest.mock import patch
from app.gui.new_contact_frame import NewContactFrame
from app.config_manager import ConfigManager
from app.sockets import ConnectionManager
from app.chat import Chat
from app.contacto import Contacto
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.fernet import Fernet
from app.cyphersuite import hash_to_string, pub_key_to_string
from app.crud import leer_contacto, insertar_contacto, leer_chats
from app.factories.chat_factory import ChatFactory
import sqlite3 as sql
import os
import random
import toga

TEST_DB = "resources/test.db"

@pytest.fixture(scope="function", autouse = True)
def crear_base_datos_para_tests():
    try:
        conn = sql.connect(TEST_DB)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE Chat(id_chat text, key text, PRIMARY KEY (id_chat))")
        conn.commit()
        conn.close()
    except sql.OperationalError:
        pass
    try:
        conn = sql.connect(TEST_DB)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE Contacto(hash text, pub_key text, ip text, PRIMARY KEY (hash))")
        conn.commit()
        conn.close()
    except sql.OperationalError:
        pass
    try:
        conn = sql.connect(TEST_DB)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE ChatContacto (id_chat text NOT NULL , hash_contacto text NULL,PRIMARY KEY (id_chat,hash_contacto) FOREIGN KEY (id_chat) REFERENCES Chat(id_chat), FOREIGN KEY (hash_contacto) REFERENCES Contacto(hash))")
        conn.commit()
        conn.close()
    except sql.OperationalError:
        pass
    yield
    try:
        os.remove(TEST_DB)
    except FileNotFoundError:
        pass

@pytest.fixture
def crear_chat() -> Chat:
    # Creamos un chat de prueba
    ConfigManager().connection_manager = ConnectionManager()
    chat = ChatFactory().produce()
    return chat

@pytest.fixture
def crear_contacto() -> Contacto:
    priv_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pub_key = priv_key.public_key()
    hash = hashes.Hash(hashes.SHA256())
    hash.update(
        pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )
    ip = "1.1.1.1"
    return Contacto(pub_key, ip, hash.finalize())
    

@patch("app.contrato.Contrato.consultar_ip")
@patch("app.crud.RUTA_BBDD", TEST_DB)
def test_add_new_contact(mock_consultar_ip, crear_chat: Chat, crear_contacto: Contacto):
    chat = crear_chat
    app = toga.App()
    frame = NewContactFrame(chat)
    app.windows.add(frame)

    mock_consultar_ip.return_value = "1.1.1.1"

    contacto = crear_contacto
    frame.key_input.value = pub_key_to_string(contacto.k_pub)
    frame.hash_input.value = hash_to_string(contacto.hash)
    frame.add_contact_to_chat(None)

    contact_list = map(
        lambda c: c.hash,
        chat.miembros
    )

    assert contacto.hash in contact_list

@patch("app.contrato.Contrato.consultar_ip")
@patch("app.crud.RUTA_BBDD", TEST_DB)
def test_add_another_new_contact(mock_consultar_ip, crear_chat: Chat, crear_contacto: Contacto):
    chat = crear_chat
    app = toga.App()
    frame = NewContactFrame(chat)
    app.windows.add(frame)

    mock_consultar_ip.return_value = "1.1.1.1"

    contacto = crear_contacto
    frame.key_input.value = pub_key_to_string(contacto.k_pub)
    frame.hash_input.value = hash_to_string(contacto.hash)
    frame.add_contact_to_chat(None)

    contact_list = map(
        lambda c: pub_key_to_string(c.k_pub),
        chat.miembros
    )

    assert pub_key_to_string(contacto.k_pub) in contact_list

@patch("app.contrato.Contrato.consultar_ip")
@patch("app.crud.RUTA_BBDD", TEST_DB)
def test_contact_added_to_db(mock_consultar_ip, crear_chat: Chat, crear_contacto: Contacto):
    chat = crear_chat
    app = toga.App()
    frame = NewContactFrame(chat)
    app.windows.add(frame)

    mock_consultar_ip.return_value = "1.1.1.1"

    contacto = crear_contacto
    frame.key_input.value = pub_key_to_string(contacto.k_pub)
    frame.hash_input.value = hash_to_string(contacto.hash)
    frame.add_contact_to_chat(None)

    db_contact = leer_contacto(hash_to_string(contacto.hash))

    assert db_contact.hash == contacto.hash

@patch("app.contrato.Contrato.consultar_ip")
@patch("app.crud.RUTA_BBDD", TEST_DB)
def test_if_contact_exists_is_not_added(mock_consultar_ip, crear_chat: Chat, crear_contacto: Contacto):
    chat = crear_chat

    app = toga.App()
    frame = NewContactFrame(chat)
    app.windows.add(frame)

    mock_consultar_ip.return_value = "1.1.1.1"

    contacto = crear_contacto
    insertar_contacto(contacto)
    
    frame.key_input.value = pub_key_to_string(contacto.k_pub)
    frame.hash_input.value = hash_to_string(contacto.hash)

    # No debe dar excepciones
    frame.add_contact_to_chat(None)

@patch("app.contrato.Contrato.consultar_ip")
@patch("app.crud.RUTA_BBDD", TEST_DB)
def test_entry_added_to_chat_contacto(mock_consultar_ip, crear_chat: Chat, crear_contacto: Contacto):
    ConfigManager().connection_manager = ConnectionManager()
    chat = ChatFactory().produce()

    app = toga.App()
    frame = NewContactFrame(chat)
    app.windows.add(frame)
    mock_consultar_ip.return_value = "1.1.1.1"

    contacto = crear_contacto
    frame.key_input.value = pub_key_to_string(contacto.k_pub)
    frame.hash_input.value = hash_to_string(contacto.hash)
    frame.add_contact_to_chat(None)

    db_chat = leer_chats()[0]
    member_hashes = map(lambda contacto: contacto.hash, db_chat.getMiembros())

    assert contacto.hash in member_hashes

@patch("app.contrato.Contrato.consultar_ip")
@patch("app.crud.RUTA_BBDD", TEST_DB)
def test_window_closes_on_method_end(mock_consultar_ip, crear_chat: Chat, crear_contacto: Contacto):
    ConfigManager().connection_manager = ConnectionManager()
    chat = ChatFactory().produce()

    app = toga.App()
    frame = NewContactFrame(chat)
    app.windows.add(frame)

    mock_consultar_ip.return_value = "1.1.1.1"

    contacto = crear_contacto
    frame.key_input.value = pub_key_to_string(contacto.k_pub)
    frame.hash_input.value = hash_to_string(contacto.hash)

    with patch.object(frame, "close") as mock_close:
        frame.add_contact_to_chat(None)
        mock_close.assert_called_once()
    