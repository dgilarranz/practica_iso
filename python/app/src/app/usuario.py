from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from python.app.src.app.mensaje import mensaje
from simplecrypt import encrypt, decrypt 

class Usuario:
    def __init__(self, hash, pub_key, priv_key):
        self.hash = hash
        self.pub_key = pub_key
        self.priv_key = priv_key
    
    def cifrar_mensaje():
        mensaje_cifrado = encrypt(priv_key, mensaje)

    def descifrar_mensaje():
        mensaje_descifrado = decrypt(priv_key,mensaje_cifrado)
