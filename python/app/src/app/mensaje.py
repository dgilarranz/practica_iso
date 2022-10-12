from datetime import datetime
import json

class Mensaje:
    def __init__(self, texto, id_chat,ttl=None):
        self.texto=texto
        self.ttl= ttl
        self.timestamp= datetime.now()
        self.id_mensaje = None          # COMPLETAR
        self.id_chat= id_chat
    
    def to_json(self) -> str:
        json_self = {
            'texto': self.texto,
            'ttl': str(self.ttl),
            'timestamp': str(self.timestamp),
            'id_mensaje': self.id_mensaje,
            'id_chat': self.id_chat
        }
        return json.dumps(json_self)

