from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from app.chat import Chat
from app.crud import insertar_chat

class ChatFactory:
    def create_chat(self):
        key = Fernet.generate_key()

        chat_hash = hashes.Hash(hashes.SHA256())
        chat_hash.update(key)
        chat_hash = chat_hash.finalize()

        chat = Chat(chat_hash, key)

        insertar_chat(chat)
        return chat