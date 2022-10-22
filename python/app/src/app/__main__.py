import asyncio
from app.chat import Chat
from app.sockets import ConnectionManager
from gui.chat_frame import ChatFrame
from app.usuario import Usuario
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives.asymmetric.padding import MGF1

# Constantes
user: Usuario = None

def crear_chat() -> Chat:
    # Creamos un chat de prueba
    chat_hash = hashes.Hash(hashes.SHA256())
    chat_hash = chat_hash.finalize()
    priv_key = rsa.generate_private_key(65537, 2049)
    pub_key = priv_key.public_key()
    return Chat(chat_hash, pub_key, priv_key, None)

if __name__ == '__main__':
    chat = crear_chat()
    frame = ChatFrame(chat)
    frame.main_loop()
