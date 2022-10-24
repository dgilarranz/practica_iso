import asyncio
from app.chat import Chat
from app.sockets import ConnectionManager
from gui.chat_frame import ChatFrame
from gui.main_frame import MainFrame
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from app.config_manager import ConfigManager
from app.setup import inicializar_usuario
import toga

def crear_chat() -> Chat:
    # Creamos un chat de prueba
    chat_hash = hashes.Hash(hashes.SHA256())
    chat_hash = chat_hash.finalize()
    key = Fernet.generate_key
    return Chat(chat_hash, key, None)

if __name__ == '__main__':
    app = toga.App()
    app.main_window = MainFrame(id="App", title="App")
    app.main_window.show()
    app.main_loop()

    
    #chat = crear_chat()
    #ConfigManager.config["user"] = inicializar_usuario()
    #frame = ChatFrame(chat)
    #frame.main_loop()
