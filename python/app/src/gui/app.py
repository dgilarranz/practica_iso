from app.chat import Chat
from gui.main_frame import MainFrame
from gui.new_chat_frame import NewChatFrame
from gui.new_contact_frame import NewContactFrame
import toga
# IMPORTS PARA PRUEBAS
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

class MessageApp(toga.App):
    
    def startup(self):
        chats = self.leer_chats()
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