import binascii
import imp
import json
from app.chat import Chat
from app.cyphersuite import cifrar_mensaje
from app.cyphersuite import descifrar_mensaje
from app.cyphersuite import hash_to_string
from app.cyphersuite import string_to_hash
from app.cyphersuite import priv_key_to_string
from app.cyphersuite import string_to_priv_key
from app.cyphersuite import pub_key_to_string
from app.cyphersuite import string_to_pub_key
from app.mensaje import Mensaje
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives.asymmetric.padding import MGF1
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives import serialization 
from cryptography.fernet import Fernet
from app.setup import inicializar_usuario
from app.config_manager import ConfigManager
from app.sockets import ConnectionManager
import pytest

@pytest.fixture
def crear_chat() -> Chat:
    # Creamos un chat de prueba
    chat_hash = hashes.Hash(hashes.SHA256())
    chat_hash = chat_hash.finalize()
    key = Fernet.generate_key()
    ConfigManager().connection_manager = ConnectionManager()
    return Chat(chat_hash, key)

def test_cifrar_mensaje(crear_chat: Chat):
    chat = crear_chat
    mensaje = Mensaje("texto prueba", binascii.hexlify(chat.id_chat).decode('utf-8'), "user_id", None)
    mensaje_cifrado = cifrar_mensaje(mensaje, chat.key)

    # Desciframos el mensaje y comprobamos que tiene los campos adecuados
    mensaje_descifrado = descifrar_mensaje(mensaje_cifrado, chat.key)
    assert mensaje_descifrado.texto == mensaje.texto

def test_descifrar_mensaje(crear_chat: Chat):
    chat = crear_chat
    mensaje = Mensaje("texto prueba", binascii.hexlify(chat.id_chat).decode('utf-8'), "id_user", None)
    
    # Ciframos el mensaje
    mensaje_cifrado = cifrar_mensaje(mensaje, chat.key)

    # Desciframos el mensaje y comprobamos si el texto es el mismo
    assert descifrar_mensaje(mensaje_cifrado, chat.key).texto == mensaje.texto

def test_hash_to_string(crear_chat: Chat):
    chat = crear_chat
    assert binascii.hexlify(chat.id_chat).decode('utf-8') == hash_to_string(chat.id_chat)

def test_priv_key_to_sring():
    priv_key = rsa.generate_private_key(65537, 2048)
    priv_key_string = binascii.hexlify(
        priv_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    ).decode('UTF-8')

    assert priv_key_string == priv_key_to_string(priv_key)


def test_pub_key_to_sring():
    priv_key = rsa.generate_private_key(65537, 2048)
    pub_key = priv_key.public_key()
    pub_key_string = binascii.hexlify(
        pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    ).decode('UTF-8')

    assert pub_key_string == pub_key_to_string(pub_key)

def test_string_to_hash(crear_chat: Chat):
    # Obtenemos una representación string del hash de chat
    chat = crear_chat
    str_hash = binascii.hexlify(chat.id_chat).decode('utf-8')

    # Verificamos que obtenemos id_chat a partir de su representación string
    assert string_to_hash(str_hash) == chat.id_chat

def test_string_to_priv_key():
    user = inicializar_usuario()
    priv_key_string = binascii.hexlify(
        user.priv_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    ).decode('UTF-8')

    assert user.priv_key.key_size == string_to_priv_key(priv_key_string).key_size

def test_string_to_pub_key():
    user = inicializar_usuario()
    pub_key_string = binascii.hexlify(
          user.pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    ).decode('UTF-8')
    assert user.pub_key.key_size == string_to_pub_key(pub_key_string).key_size

