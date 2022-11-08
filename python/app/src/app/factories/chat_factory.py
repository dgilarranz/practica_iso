from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from app.chat import Chat
from app.crud import insertar_chat
from app.cyphersuite import string_to_hash
from sqlite3 import IntegrityError
from app.factories.factory import Factory

class ChatFactory(Factory):
    
    def __init__(self, id_str = None, key_str = None):
        self.id_str = id_str
        self.key_str = key_str

    def produce(self) -> Chat:
        if (self.id_str is None and self.key_str is None):
            chat = self.create_new_chat()
        else:
            chat = self.add_chat_using_data()

        try:
            insertar_chat(chat)
        except IntegrityError:
            raise ChatExistsException()
        
        return chat
    
    def add_chat_using_data(self) -> Chat:
        key = string_to_hash(self.key_str)
        chat_hash = string_to_hash(self.id_str)

        return Chat(chat_hash, key)
    
    def create_new_chat(self):
        key = Fernet.generate_key()

        chat_hash = hashes.Hash(hashes.SHA256())
        chat_hash.update(key)
        chat_hash = chat_hash.finalize()

        return Chat(chat_hash, key)



class ChatExistsException(Exception):
    pass