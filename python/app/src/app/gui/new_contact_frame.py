import toga
from toga.style import Pack
from toga.style.pack import COLUMN

class NewContactFrame(toga.Window):
    def __init__(self) -> None:
        super().__init__(title="Nuevo contacto")
        main_box = toga.Box(id="main_box", style=Pack(direction=COLUMN, background_color="#155757"))

        createcont = self.crearContacto()

        main_box.add(createcont)
        self.content = main_box
        self.content.refresh()

    def crearContacto(self) -> toga.Box:
        id_createcont_box = toga.Box(style=Pack(padding=10))
        clave_createcont_box = toga.Box(style=Pack(padding=10))
        box_createcont = toga.Box(style=Pack(direction=COLUMN))

        id_createcont_input = toga.TextInput(style=Pack(flex=1))
        clave_createcont_input = toga.TextInput(style=Pack(flex=1))

        id_createcont_label = toga.Label('ID contacto:', style=Pack(padding_left = 5, padding_right = 30))
        clave_createcont_label = toga.Label('Clave Pública:', style=Pack(padding_left = 5, padding_right = 10))

        createcont_button = toga.Button('Añadir')

        id_createcont_box.add(id_createcont_label)
        id_createcont_box.add(id_createcont_input)

        clave_createcont_box.add(clave_createcont_label)
        clave_createcont_box.add(clave_createcont_input)

        box_createcont.add(id_createcont_box)
        box_createcont.add(clave_createcont_box)
        box_createcont.add(createcont_button)

        return box_createcont
