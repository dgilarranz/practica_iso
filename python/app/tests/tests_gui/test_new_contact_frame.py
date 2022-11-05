import pytest
from unittest.mock import patch
from app.gui.new_contact_frame import NewContactFrame
from app.chat import Chat
from app.contacto import Contacto
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.fernet import Fernet
from app.cyphersuite import hash_to_string, pub_key_to_string

@pytest.fixture
def crear_chat() -> Chat:
    # Creamos un chat de prueba
    chat_hash = hashes.Hash(hashes.SHA256())
    chat_hash = chat_hash.finalize()
    key = Fernet.generate_key()
    return Chat(chat_hash, key)

@pytest.fixture
def crear_contacto() -> Contacto:
    priv_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pub_key = priv_key.public_key()
    hash = hashes.Hash(hashes.SHA256())
    ip = "1.1.1.1"
    return Contacto(pub_key, ip, hash.finalize())
    

@patch("app.contrato.Contrato.consultar_ip")
def test_add_new_contact(mock_consultar_ip, crear_chat: Chat, crear_contacto: Contacto):
    chat = crear_chat
    frame = NewContactFrame(chat)

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
def test_add_another_new_contact(mock_consultar_ip, crear_chat: Chat, crear_contacto: Contacto):
    chat = crear_chat
    frame = NewContactFrame(chat)

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
