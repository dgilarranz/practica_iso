import asyncio
from email import message
import json
from xmlrpc.client import Boolean
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives.asymmetric.padding import MGF1
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.fernet import Fernet
from app.cyphersuite import hash_to_string
from app.mensaje import Mensaje
from app.sockets import ConnectionManager
import binascii

class Chat:
    def __init__(self, id_chat, key: Fernet, cm: ConnectionManager = None):
        self.id_chat= id_chat
        self.miembros=set()
        self.key = key
        self.cm = cm
        self.messages = []


    def addMiembro(self,contacto):
        self.miembros.add(contacto)

    def getMiembros(self):
        return self.miembros

    def getID_Chat(self):
        return self.id_chat

    # Devuelve el número de mensajes enviados
    async def send_message(self, mensaje: Mensaje) -> int:
        # Ciframos el mensaje
        mensaje_cifrado = binascii.hexlify(
            self.key.encrypt(mensaje.to_json().encode("utf-8"))
        ).decode('utf-8')

        # Enviamos un mensaje a todos los miembros
        pending_tasks = set()
        sent_messages = 0
        for m in self.miembros:
            task = asyncio.create_task(self.cm.send_message(
                ip=m.direccion_ip, port=self.cm.port,
                contact_hash=hash_to_string(self.id_chat), message=mensaje_cifrado
            ))
            pending_tasks.add(task)

        # Esperamos a que se completen los envíos
        for task in pending_tasks:
            await task
            sent_messages += 1
        
        # Devolvemos el número de mensajes enviados
        return sent_messages

    # Devuelve la lista de mensajes leídos
    def read_new_messages(self) -> list[Mensaje]:
        # Obtenemos los mensajes nuevos para nuestro chat
        encrypted_messages = self.cm.get_messages(hash_to_string(self.id_chat))
        decrypted_messages = []

        for message in encrypted_messages:
            json_message = json.loads(
                self.key.decrypt(message.encode("utf-8"))
            )
            decrypted_messages.append(
                Mensaje(
                    id_chat=json_message['id_chat'],
                    texto=json_message['texto'],
                    ttl=json_message['ttl'],
                    id_sender=json_message['id_sender']
                )
            )

        return decrypted_messages
            
