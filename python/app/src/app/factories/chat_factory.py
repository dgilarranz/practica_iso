from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from app.chat import Chat
from app.crud import insertar_chat
from app.cyphersuite import string_to_hash

class ChatFactory:
    def create_chat(self, id_str = None, key_str = None) -> Chat:
        if (key_str is None):
            key = Fernet.generate_key()
        else:
            key = string_to_hash(key_str)

        if (id_str is None):
            chat_hash = hashes.Hash(hashes.SHA256())
            chat_hash.update(key)
            chat_hash = chat_hash.finalize()
        else:
            chat_hash = string_to_hash(id_str)

        chat = Chat(chat_hash, key)
        insertar_chat(chat)
        return chat

class ChatExistsException(Exception):
    pass