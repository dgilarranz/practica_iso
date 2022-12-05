import asyncio
from xmlrpc.client import Boolean
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives.asymmetric.padding import MGF1
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.fernet import Fernet
from app.cyphersuite import hash_to_string, cifrar_mensaje, descifrar_mensaje
from app.mensaje import Mensaje
from app.config_manager import ConfigManager
from app.observer import Observer, Subject

class Chat(Observer, Subject):
    def __init__(self, id_chat, key: bytes):
        super().__init__()
        self.id_chat= id_chat
        self.miembros=set()
        self.key = key
        self.messages = []

        # Subscribimos el chat a ConnectionManager (Patrón Observer)
        ConfigManager().connection_manager.subscribe(self)


    def addMiembro(self,contacto):
        self.miembros.add(contacto)

    def getMiembros(self):
        return self.miembros

    def getID_Chat(self):
        return self.id_chat

    # Devuelve el número de mensajes enviados
    async def send_message(self, mensaje: Mensaje) -> int:
        # Ciframos el mensaje
        mensaje_cifrado = cifrar_mensaje(mensaje, self.key)

        # Enviamos un mensaje a todos los miembros
        cm = ConfigManager().connection_manager
        pending_tasks = set()
        sent_messages = 0
        for m in self.miembros:
            task = asyncio.create_task(cm.send_message(
                ip=m.direccion_ip, port=cm.port,
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
        encrypted_messages = ConfigManager().connection_manager.get_messages(hash_to_string(self.id_chat))
        decrypted_messages = []

        for message in encrypted_messages:
            message = descifrar_mensaje(message, self.key)
            decrypted_messages.append(message)

        return decrypted_messages
    
    def update(self) -> None:
        new_messages = self.read_new_messages()

        for msg in new_messages:
            msg_cifrado = cifrar_mensaje(mensaje=msg, key=ConfigManager().user.key)
            from app.crud import insertar_mensaje
            insertar_mensaje(msg_cifrado)

        self.messages.extend(new_messages)
        self.notify()
            
