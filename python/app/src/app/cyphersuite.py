import binascii
import json
from app.mensaje import Mensaje
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives.asymmetric.padding import MGF1
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization 
from cryptography.fernet import Fernet
from app.usuario import Usuario
from app.contacto import Contacto


def cifrar_mensaje(mensaje: Mensaje, key: bytes) -> str:
    return binascii.hexlify(
            Fernet(key).encrypt(mensaje.to_json().encode("utf-8"))
        ).decode('utf-8')

def descifrar_mensaje(mensaje_cifrado: str, key: bytes) -> Mensaje:
    mensaje_descifrado = Fernet(key).decrypt(binascii.unhexlify(mensaje_cifrado.encode('utf-8')))
    return Mensaje.from_json(mensaje_descifrado)

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

def cifrar_ip(user: Usuario, ip: str):
    ip_cifrada = user.pub_key.encrypt(
        str.encode(ip, 'utf-8'),
        OAEP(
            mgf=MGF1(SHA256()),
            algorithm=SHA256(),
            label=None
        )
    )
    return hash_to_string(ip_cifrada)

def descifrar_ip(contacto: Contacto, ip_cifrada: str):
    return "1.1.1.1"
