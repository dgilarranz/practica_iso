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

# IMPORTS PARA PRUEBAS
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

class MessageApp(toga.App):

    def startup(self):
        self.cargar_configuracion()
        self.chats = leer_chats()
        self.leer_mensajes(self.chats)

        self.main_window = MainFrame("main_window", "App", self.chats)

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

    def cargar_configuracion(self):
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
            ConfigManager.config["user"] = user

    def leer_mensajes(self, chats: list[Chat]):
        # mensajes = leer_mensaje()
        # Ordenamos los mensajes por tiempo
        mensajes = []
        mensajes = sorted(mensajes, key=lambda msg: msg.timestamp)
        for msg in mensajes:
            chat = list(filter(lambda chat, msg: chat.id_chat == msg.id_chat, chats))[0]
            chat.messages.append(msg)

    def leer_contactos(self, chats: list[Chat]):
        pass

        
        

        
            
            
