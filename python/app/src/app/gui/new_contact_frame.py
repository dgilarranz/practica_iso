import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from app.chat import Chat
from app.contacto import Contacto
from app.contrato import Contrato
from app.cyphersuite import string_to_hash, string_to_priv_key, descifrar_ip
from app.crud import insertar_contacto, insertar_chat_contacto
from app.config_manager import ConfigManager
import sqlite3

class NewContactFrame(toga.Window):
    def __init__(self, chat: Chat) -> None:
        self.chat = chat
        self.pub_key = ""
        self.contact_hash = ""
        

        super().__init__(title="Nuevo contacto")
        main_box = toga.Box(id="main_box", style=Pack(direction=COLUMN))

        createcont = self.crearContacto()

        main_box.add(createcont)
        self.content = main_box
        self.content.refresh()

    def crearContacto(self) -> toga.Box:
        id_createcont_box = toga.Box(style=Pack(padding=10))
        clave_createcont_box = toga.Box(style=Pack(padding=10))
        box_createcont = toga.Box(style=Pack(direction=COLUMN))

        self.hash_input = id_createcont_input = toga.TextInput(style=Pack(flex=1))
        self.key_input = clave_createcont_input = toga.TextInput(style=Pack(flex=1))

        id_createcont_label = toga.Label('ID contacto:', style=Pack(padding_left = 5, padding_right = 30))
        clave_createcont_label = toga.Label('Clave Pública:', style=Pack(padding_left = 5, padding_right = 10))

        createcont_button = toga.Button('Añadir', on_press=self.add_contact_to_chat)

        id_createcont_box.add(id_createcont_label)
        id_createcont_box.add(id_createcont_input)

        clave_createcont_box.add(clave_createcont_label)
        clave_createcont_box.add(clave_createcont_input)

        box_createcont.add(id_createcont_box)
        box_createcont.add(clave_createcont_box)
        box_createcont.add(createcont_button)

        return box_createcont
    
    def add_contact_to_chat(self, widget):
        pub_key = self.key_input.value
        contact_hash = self.hash_input.value
        contacto = Contacto(
            string_to_priv_key(pub_key), 
            "", 
            string_to_hash(contact_hash)
        )

        direccion_ip = ConfigManager().contrato.consultar_ip(contact_hash)
        contacto.direccion_ip = descifrar_ip(contacto, direccion_ip)

        try:
            insertar_contacto(contacto)
        except sqlite3.IntegrityError as e:
            pass
            
        try:
            insertar_chat_contacto(self.chat, contacto)
        except sqlite3.IntegrityError:
            pass

        self.chat.addMiembro(contacto)
        self.close()
