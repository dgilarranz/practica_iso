import imp
import os
from pkgutil import extend_path
import resource
import sqlite3
import sys
import toga
import pathlib
from app.chat import Chat
from app.crud import leer_chat, leer_mensaje
from app.gui.main_frame import MainFrame
from app.gui.new_chat_frame import NewChatFrame
from app.gui.new_contact_frame import NewContactFrame
from app.setup import inicializar_usuario
from app.file_manager import guardar_usuario, leer_usuario
from app.cyphersuite import hash_to_string
from app.config_manager import ConfigManager
from app.crud import leer_mensaje, leer_chats, createDB, RUTA_BBDD
from app.sockets import ConnectionManager
import asyncio

class MessageApp(toga.App):

    def startup(self):
        self.cargar_configuracion()
        self.chats = leer_chats()
        self.leer_mensajes(self.chats)

        self.main_window = MainFrame("main_window", "App", self.chats)
        self.main_window.show()

    def cargar_configuracion(self):
        self.cargar_usuario()
        self.arrancar_servidor()
    
    def cargar_usuario(self):
        user = None

        # Investigar mejor solución. Temporalmente, cambiar la ejecución al directorio python/app
        correct_path = pathlib.Path(__file__).parent.resolve().parent.resolve().parent.resolve().parent.resolve()
        os.chdir(correct_path)
        print(correct_path)

        try:
            createDB()
        except sqlite3.OperationalError:
            pass

        try:
            user = leer_usuario()
        except FileNotFoundError:
            user = inicializar_usuario()
            guardar_usuario(user)
        finally:
            ConfigManager().user = user

    def arrancar_servidor(self):
        cm = ConnectionManager()
        asyncio.create_task(cm.start_service(), name="servidor")
        ConfigManager().connection_manager = cm

    def leer_mensajes(self, chats: list[Chat]):
        # Ordenamos los mensajes por tiempo
        mensajes = leer_mensaje()
        mensajes = sorted(mensajes, key=lambda msg: msg.timestamp)
        for msg in mensajes:
            chat = list(filter(lambda chat: hash_to_string(chat.id_chat) == msg.id_chat, chats))[0]
            chat.messages.append(msg)


        
        

        
            
            
