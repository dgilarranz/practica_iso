import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class MainFrame(toga.MainWindow):
    def __init__(self, id, title) -> None:
        super().__init__(id, title)
        self.create_interface()

    def create_interface(self):
        main_box = toga.Box(id="main_box", style=Pack(direction=COLUMN, background_color="#155757"))

        options_box = self.create_options_box()
        self.chats_box = self.create_chats_box()
        divider = toga.Divider(direction=0, style=Pack(height=3))
        main_box.add(options_box, divider, self.chats_box)

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
        return toga.Box()
    
    def open_add_chat_window(self, widget):
        pass

    def open_user_window(self, widget):
        pass

    def open_chat_window(self, widget):
        pass

