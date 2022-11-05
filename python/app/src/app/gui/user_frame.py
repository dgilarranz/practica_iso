import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class UserFrame(toga.Window):
    def __init__(self, user_id: str, pub_key: str):
        super().__init__()
        self.inicializar_gui(user_id, pub_key)

    def inicializar_gui(self, user_id: str, pub_key: str):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        id_box = toga.Box(style=Pack(padding=10, direction=COLUMN))
        id_label = toga.Label("ID:", style=Pack(padding_left=5))
        id_textfield = toga.TextInput(readonly=True, style=Pack(padding_left=5, padding_right=5, flex=1))
        id_textfield.value = user_id
        id_box.add(id_label, id_textfield)

        key_box = toga.Box(style=Pack(padding=10, direction=COLUMN))
        key_label = toga.Label("Public Key:", style=Pack(padding_left=5))
        key_textfield = toga.MultilineTextInput(readonly=True, style=Pack(padding_left=5, padding_right=5, flex=1))
        key_textfield.MIN_HEIGHT = 300
        key_textfield.value = pub_key
        key_box.add(key_label, key_textfield)

        main_box.add(id_box, key_box)

        self.content = main_box
