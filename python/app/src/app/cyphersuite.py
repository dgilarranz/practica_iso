import binascii
import json
from app.mensaje import Mensaje
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives.asymmetric.padding import MGF1
from cryptography.hazmat.primitives.hashes import SHA256

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