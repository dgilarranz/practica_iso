from datetime import datetime

class Mensaje:
    def __init__(self, texto, id_chat,ttl=None):
        self.texto=texto
        self.ttl= ttl
        self.timestamp= datetime.now()
        self.id_mensaje
        self.id_chat= id_chat

