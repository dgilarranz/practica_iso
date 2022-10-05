from app.usuario import Usuario
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives.asymmetric.padding import MGF1
from cryptography.hazmat.primitives.hashes import SHA256
import requests

def inicializar_usuario():
    priv_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    pub_key = priv_key.public_key()

    # Obtenemos el hash del usuario a partir de su clave pública
    user_hash = hashes.Hash(hashes.SHA256())
    user_hash.update(
        pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )
    
    user = Usuario(user_hash.finalize(), pub_key, priv_key)
    return user

def obtener_ip():
    response = requests.get("http://ifconfig.me")
    return response.text

def cifrar_ip(user: Usuario):
    return user.pub_key.encrypt(
        str.encode(obtener_ip(), 'utf-8'),
        OAEP(
            mgf=MGF1(SHA256()),
            algorithm=SHA256(),
            label=None
        )
    )
