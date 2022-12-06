import toga
from toga.style import Pack
from toga.style.pack import COLUMN

class MoneyFrame(toga.Window):
    
    def __init__(self):
        super().__init__()

        main_box = toga.Box(style=Pack(direction=COLUMN))
        from_box = self.create_box("From Address:")
        key_box = self.create_box("Private Key:")
        token_box = self.create_box("Token Address:")

        join_button = toga.Button('Unirse al chat', on_press=None)

        main_box.add(from_box)
        main_box.add(key_box)
        main_box.add(token_box)
        self.content = main_box



    def create_box(self, label_text: str) -> toga.Box:
        label = toga.Label(label_text, style=Pack(padding_left = 5, padding_right = 50))
        input = toga.TextInput(style=Pack(flex=1))
        
        box = toga.Box(style=Pack(direction=COLUMN))
        box.add(label)
        box.add(input)
        return box