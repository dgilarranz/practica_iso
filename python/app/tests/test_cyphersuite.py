import binascii
import json
from app.chat import Chat
from app.cyphersuite import cifrar_mensaje
from app.cyphersuite import descifrar_mensaje
from app.mensaje import Mensaje
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives.asymmetric.padding import MGF1
from cryptography.hazmat.primitives.hashes import SHA256
import pytest

@pytest.fixture
def crear_chat() -> Chat:
    # Creamos un chat de prueba
    chat_hash = hashes.Hash(hashes.SHA256())
    chat_hash = chat_hash.finalize()
    priv_key = rsa.generate_private_key(65537, 2049)
    pub_key = priv_key.public_key()
    return Chat(chat_hash, pub_key, priv_key)

def test_cifrar_mensaje(crear_chat: Chat):
    chat = crear_chat
    mensaje = Mensaje("texto prueba", binascii.hexlify(chat.id_chat).decode('utf-8'), None)
    mensaje_cifrado = cifrar_mensaje(mensaje, chat.pub_key)

    # Desciframos el mensaje y comprobamos que tiene los campos adecuados
    mensaje_descifrado = json.loads(
        chat.priv_key.decrypt(
            ciphertext=binascii.unhexlify(mensaje_cifrado.encode('utf-8')),
                padding=OAEP(
                mgf=MGF1(SHA256()),
                algorithm=SHA256(),
                label=None
            )
        )
    )
    assert mensaje_descifrado['texto'] == mensaje.texto

def test_descifrar_mensaje(crear_chat: Chat):
    chat = crear_chat
    mensaje = Mensaje("texto prueba", binascii.hexlify(chat.id_chat).decode('utf-8'), None)
    
    # Ciframos el mensaje
    mensaje_cifrado = binascii.hexlify(
        chat.pub_key.encrypt(
            mensaje.to_json().encode('utf-8'),
            padding=OAEP(
                mgf=MGF1(SHA256()),
                algorithm=SHA256(),
                label=None
            )
        )
    ).decode("utf-8")

    # Desciframos el mensaje y comprobamos si el texto es el mismo
    assert descifrar_mensaje(mensaje_cifrado, chat.priv_key).texto == mensaje.texto