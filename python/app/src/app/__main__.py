import asyncio
from app.chat import Chat
from app.sockets import ConnectionManager
from app.gui.app import MessageApp
from app.gui.chat_frame import ChatFrame
from app.gui.main_frame import MainFrame
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from app.config_manager import ConfigManager
from app.setup import inicializar_usuario
import toga
import asyncio

if __name__ == '__main__':
    app = MessageApp()
    app.main_loop()