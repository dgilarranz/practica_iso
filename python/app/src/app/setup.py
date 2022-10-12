from app.usuario import Usuario
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives.asymmetric.padding import MGF1
from cryptography.hazmat.primitives.hashes import SHA256
import requests
import socket

def inicializar_usuario() -> Usuario:
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

def obtener_ip() -> str:
    response = requests.get("http://ifconfig.me")
    return response.text

def cifrar_ip(user: Usuario, ip: str) -> bytes:
    return user.pub_key.encrypt(
        str.encode(ip, 'utf-8'),
        OAEP(
            mgf=MGF1(SHA256()),
            algorithm=SHA256(),
            label=None
        )
    )

def obtener_ip_privada() -> str:
    # Abrimos un socket a una IP cualquiera (Interna) y obtenemos la ip local
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    ip = ''
    try:
        s.connect(('192.168.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        # Si hay errores, devolvemos la ip de localhost
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip
    
