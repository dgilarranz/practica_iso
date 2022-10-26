import asyncio
from app.chat import Chat
from app.sockets import ConnectionManager
from gui.app import MessageApp
from gui.chat_frame import ChatFrame
from gui.main_frame import MainFrame
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from app.config_manager import ConfigManager
from app.setup import inicializar_usuario
import toga

if __name__ == '__main__':
    app = MessageApp()
    app.main_loop()
