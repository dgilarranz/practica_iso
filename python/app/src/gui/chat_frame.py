from cgitb import text
from ctypes import alignment
from curses.textpad import Textbox
from distutils.log import info
from turtle import st, width
from app.mensaje import Mensaje
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from app.chat import Chat
from app.cyphersuite import hash_to_string
import copy
from app.__main__ import user

class ChatFrame(toga.App):

    def __init__(self, chat: Chat) -> None:
        super().__init__()
        self.chat = chat
        self.max_chars_per_line = 50
        

    def startup(self) -> None:
        """Método que inicializa la interfaz gráfica"""
        self.main_window = toga.MainWindow(title="PRUEBA")
        main_box = toga.Box(id="main_box", style=Pack(direction=COLUMN, background_color="#155757"))
        self.main_window.content = main_box

        info_box = self.create_info_box()
        message_box = self.create_message_box()
        text_box = self.create_text_box()
        main_box.add(
            info_box, 
            toga.Divider(direction=0, style=Pack(height=3)),
            message_box,
            toga.Divider(direction=0, style=Pack(height=3)),
            text_box
        )

        self.add_message("Holaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "self")
        self.add_message("Hola", "other")
        
        self.main_window.content.refresh()
        print(str(message_box.content))
        self.main_window.show()

    def create_info_box(self)-> toga.Box:
        info_box = toga.Box(id="main_box", style=Pack(direction=ROW, background_color="#155757", padding=10))
        
        chat_title_label = toga.Label(text="Chat", style=Pack(padding_right=10, font_weight="bold"))
        chat_id = hash_to_string(self.chat.id_chat)
        chat_id_label = toga.Label(text=chat_id)

        add_contact_button = toga.Button(
            text="+",
            on_press=self.add_contact,
            style=Pack(alignment="right", padding_left=10, padding_right=10)
        )

        send_crypto_button = toga.Button(
            text="$",
            on_press=self.send_crypto,
            style=Pack(alignment="right", padding_left=10, padding_right=10)
        )

        info_box.add(chat_title_label)
        info_box.add(chat_id_label)
        info_box.add(add_contact_button)
        info_box.add(send_crypto_button)

        return info_box

    def create_message_box(self) -> toga.ScrollContainer:
        content = toga.Box(id="message_box", style=Pack(direction=COLUMN))
        self.message_container = content
        message_box = toga.ScrollContainer(content=content, horizontal=False, style=Pack(flex=1))
        return message_box

    def create_text_box(self) -> toga.Box:
        text_box = toga.Box(id="text_box", style=Pack(direction=ROW, padding=10))
        
        message_input = toga.TextInput(
            id="message_input_field",
            placeholder="Escribe un mensaje",
            style=Pack(flex=1)
        )
        send_button = toga.Button(
            text="Enviar",
            on_press=self.send_message,
            style=Pack(alignment="right", padding_left=10, padding_right=10)
        )
        text_box.add(message_input)
        text_box.add(send_button)
        self.message_input = message_input

        return text_box

    def add_contact(self, widget):
        pass

    def send_crypto(self, widget):
        pass

    def send_message(self, widget):
        message_content = self.message_input.value
        message = Mensaje(message_content, self.chat.id_chat, hash_to_string(user.hash))

        self.chat.messages.append(message)
        self.chat.send_message(message)

    def add_message(self, message, sender):
        # La longitud máxima de cada línea serán 50 chars, si es más, se parte el mensaje
        lines = []
        current_line = " "                          # Las líneas empezarán con un espacio
        for i in range(0, len(message)):
            print(i)
            if len(current_line) < self.max_chars_per_line - 2:
                current_line += message[i]
            else:
                lines.append(current_line + " ")    # ... y terminan con espacio
                current_line = " " + message[i]
        # Añadimos la última línea
        lines.append(current_line + " ")        
        print(lines)

        # Estilo general para todas las líneas
        style = Pack(height=30)
        if sender == user.hash:
            style.update(alignment="right")
            style.update(padding_left=400)
            style.update(padding_right=10)
            style.update(background_color="#125754")
        else:
            style.update(alignment="left")
            style.update(padding_right=400)
            style.update(padding_left=10)
            style.update(background_color="#472b45")
        
        # Creamos un widget por línea
        for line in lines:
            line_style = copy.copy(style)
            # Si es la primera línea, añadimos un padding superior de 10
            if line == lines[0]:
                line_style.update(padding_top=10)

            # Si es la última o única línea, añadimos un padding inferior de 10
            if line == lines[len(lines) - 1]:
                line_style.update(padding_bottom=10)
            
            message_widget = toga.Label(text=line, style=line_style)
            self.message_container.add(message_widget)

        self.main_window.content.refresh()
        
        


    
