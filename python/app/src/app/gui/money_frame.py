import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from app.erc20andEthSender import MoneyContract

class MoneyFrame(toga.Window):
    
    def __init__(self):
        super().__init__()

        main_box = toga.Box(style=Pack(direction=COLUMN))
        self.from_box = self.create_box("From Address:")
        self.key_box = self.create_box("Private Key:")
        self.token_box = self.create_box("Token Address:")
        self.eth_box = self.create_box("Eth Ammount:")
        self.to_box = self.create_box("To Address:")

        send_button = toga.Button("Send", on_press=self.send_money)

        main_box.add(self.from_box)
        main_box.add(self.key_box)
        main_box.add(self.token_box)
        main_box.add(self.eth_box)
        main_box.add(self.to_box)
        main_box.add(send_button)
        self.content = main_box

    def create_box(self, label_text: str) -> toga.Box:
        label = toga.Label(label_text, style=Pack(padding_left = 5, padding_right = 50))
        input = toga.TextInput(style=Pack(flex=1))
        
        box = toga.Box(style=Pack(direction=COLUMN))
        box.add(label)
        box.add(input)
        return box

    def send_money(self, widget):
        MoneyContract(
            self.from_box.children[1].value,
            self.key_box.children[1].value,
            self.token_box.children[1].value,
            float(self.eth_box.children[1].value),
            self.to_box.children[1].value
        )