import os
from app.chat import Chat
from gui.main_frame import MainFrame
from gui.new_chat_frame import NewChatFrame
from gui.new_contact_frame import NewContactFrame
from app.setup import inicializar_usuario
from app.file_manager import guardar_usuario, leer_usuario
from app.cyphersuite import hash_to_string
from app.config_manager import ConfigManager
import toga
# IMPORTS PARA PRUEBAS
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

class MessageApp(toga.App):

    def startup(self):
        self.cargar_configuracion()
        self.chats = self.leer_chats()
        self.leer_mensajes(self.chats)
        self.leer_contactos(self.chats)


        self.main_window = MainFrame("main_window", "App", chats)

        # Pruebas ventanas ##############################
        new_chat_window = NewChatFrame()
        new_chat_window.app = self

        new_contact_window = NewContactFrame()
        # new_contact_window.app = self
        # new_contact_window.show()

        self.windows = [ new_chat_window, new_contact_window]
        for w in self.windows:
            try:
                w.show()
            except Exception:
                print("Ventana aún no implementada")

        #################################################

        self.main_window.show()
    
    def leer_chats(self) -> list[Chat]:
        # IMPLEMENTACIÓN PRUEBA -> REAL: LEER BBDD
        chat_hash = hashes.Hash(hashes.SHA256())
        chat_hash = chat_hash.finalize()
        key = Fernet.generate_key
        return [Chat(chat_hash, key, None)]

    def cargar_configuracion(self):
        user = None
        if not os.path.isfile("app/resources/config.json"):
            user = inicializar_usuario()
            guardar_usuario(user)
        else:
            user = leer_usuario()
        
        ConfigManager["user"] = hash_to_string(user.hash)

    def leer_mensajes(self, chats: list[Chat]):
        pass

    def leer_contactos(self, chats: list[Chat]):
        pass

        
        

        
            
            
