import binascii
import json
from app.mensaje import Mensaje
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives.asymmetric.padding import MGF1
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization 


def cifrar_mensaje(mensaje: Mensaje, pub_key: RSAPublicKey) -> str:
    return binascii.hexlify(
            pub_key.encrypt(
                mensaje.to_json().encode('utf-8'),
                padding=OAEP(
                    mgf=MGF1(SHA256()),
                    algorithm=SHA256(),
                    label=None
                )
            )
        ).decode('utf-8')

def descifrar_mensaje(mensaje_cifrado: str, priv_key: RSAPrivateKey) -> Mensaje:
    mensaje_descifrado = json.loads(
        priv_key.decrypt(
            ciphertext=binascii.unhexlify(mensaje_cifrado.encode('utf-8')),
                padding=OAEP(
                mgf=MGF1(SHA256()),
                algorithm=SHA256(),
                label=None
            )
        )
    )
    return Mensaje(
        texto=mensaje_descifrado['texto'],
        id_chat=mensaje_descifrado['id_chat'],
        ttl=mensaje_descifrado['ttl']
    )

def hash_to_string(hash: bytes) -> str:
    return binascii.hexlify(hash).decode('utf-8')

def string_to_hash(string: str) -> bytes:
    return binascii.unhexlify(string.encode('utf-8'))

def priv_key_to_string(key: RSAPrivateKey) -> str:
    return binascii.hexlify(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    ).decode('UTF-8')

def string_to_priv_key(string: str) -> RSAPrivateKey:
    return serialization.load_pem_private_key(
        binascii.unhexlify(string.encode('utf-8')),
        None
    )

def pub_key_to_string(key: RSAPublicKey) -> str:
    return binascii.hexlify(
        key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    ).decode('UTF-8')

def string_to_pub_key(string: str) -> RSAPublicKey:
    return serialization.load_pem_public_key(
        binascii.unhexlify(string.encode('utf-8'))
    )
