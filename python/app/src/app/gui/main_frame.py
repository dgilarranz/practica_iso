from tkinter import HORIZONTAL
from tkinter.ttk import Style
from app.chat import Chat
from app.gui.chat_frame import ChatFrame
from app.cyphersuite import hash_to_string, pub_key_to_string
from app.gui.new_chat_frame import NewChatFrame
from app.gui.user_frame import UserFrame
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from app.config_manager import ConfigManager

class MainFrame(toga.MainWindow):
    def __init__(self, id: str, title: str, chat_list: list[Chat]) -> None:
        super().__init__(id, title)
        self.chat_list = chat_list
        self.btn_chat_map = {}
        self.create_interface()

    def create_interface(self):
        main_box = toga.Box(id="main_box", style=Pack(direction=COLUMN, background_color="#155757"))

        options_box = self.create_options_box()
        chats_scroll_box = self.create_chats_box()
        divider = toga.Divider(direction=0, style=Pack(height=3))
        main_box.add(options_box, divider, chats_scroll_box)

        self.content = main_box
        self.content.refresh()

    def create_options_box(self):
        options_box = toga.Box(id="options_box", style=Pack(direction=ROW, padding=10))

        add_chat_button = toga.Button(
            id="add_chat_button",
            text="+",
            style=Pack(padding_left=10, padding_right=10),
            on_press=self.open_add_chat_window
        )
        user_config_button = toga.Button(
            id="user_config_button",
            text="Usuario",
            style=Pack(padding_left=10, padding_right=10), 
            on_press=self.open_user_window
        )

        options_box.add(add_chat_button, user_config_button)
        return options_box

    def create_chats_box(self):
        self.chats_box = toga.Box(id="options_box", style=Pack(direction=COLUMN, padding=10, flex=1))
        scroll_container = toga.ScrollContainer(
            content=self.chats_box,
            horizontal=False,
            style=Pack(flex=1)
        )

        for chat in self.chat_list:
            self.chats_box.add(self.create_chat_widget(chat))

        return scroll_container
    
    def open_add_chat_window(self, widget):
        window = NewChatFrame()
        window.app = self.app
        window.show()

    def open_user_window(self, widget):
        user = ConfigManager.config["user"]
        window = UserFrame(hash_to_string(user.hash), pub_key_to_string(user.pub_key))
        window.app = self.app
        window.show()

    def create_chat_widget(self, chat: Chat) -> toga.Box:
        str_chat_id = hash_to_string(chat.id_chat)
        chat_box = toga.Box(id=f"chat_{str_chat_id}_box", style=Pack(direction=COLUMN))

        inner_box = toga.Box(id=f"chat_{str_chat_id}_inner_box", style=Pack(direction=ROW, padding=10))
        label_chat = toga.Label("Chat:", style=Pack(font_weight="bold", padding_right=5))
        label_id = toga.Label(str_chat_id, style=Pack(width=950))
        open_button = toga.Button(
            text="Abrir",
            id=f"open_{str_chat_id}_btn",
            style=Pack(padding_left=20),
            on_press=self.open_chat
        )
        self.btn_chat_map[open_button.id] = chat

        inner_box.add(label_chat, label_id, open_button)
        chat_box.add(inner_box, toga.Divider(direction=0, style=Pack(height=2)))
        return chat_box
        

    def open_chat(self, widget) -> None:
        chat = self.btn_chat_map[widget.id]
        chat_window = ChatFrame(chat)
        chat_window.app = self.app
        chat_window.show()


