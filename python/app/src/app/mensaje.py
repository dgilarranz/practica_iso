from datetime import datetime
import json
import uuid

class Mensaje:
    def __init__(self, texto, id_chat, id_sender, ttl=None):
        self.texto=texto
        self.ttl= ttl
        self.timestamp= datetime.now()
        self.id_mensaje = uuid.uuid4()
        self.id_chat= id_chat
        self.id_sender = id_sender
    
    def to_json(self) -> str:
        json_self = {
            'texto': self.texto,
            'ttl': str(self.ttl),
            'timestamp': str(self.timestamp),
            'id_mensaje': str(self.id_mensaje),
            'id_chat': self.id_chat,
            'id_sender': self.id_sender
        }
        return json.dumps(json_self)

