from cgitb import text
from tkinter.ttk import Style
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class ChatFrame(toga.App):
    def startup(self):
        """Método que inicializa la interfaz gráfica"""
        main_box = toga.Box(id="main_box", style=Pack(direction=COLUMN))

        info_box = self.create_info_box()
        message_box = self.create_message_box()
        text_box = self.create_text_box()

        main_box.add(info_box, message_box, text_box)
        self.main_window = toga.MainWindow(title="PRUEBA")
        self.main_window.content = main_box
        self.main_window.show()

    def create_info_box(self)-> toga.Box:
        info_box = toga.Box(id="info_box", style=Pack(direction=ROW))
        # resto
        return info_box

    def create_message_box(self) -> toga.ScrollContainer:
        content = toga.Box(id="message_box", style=Pack(direction=COLUMN))
        message_box = toga.ScrollContainer(content)
        # Resto
        return message_box

    def create_text_box(self) -> toga.Box:
        text_box = toga.Box(id="text_box", style=Pack(direction=COLUMN))
        # resto
        return text_box


    
