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
        id_createcont_box = toga.Box()
        clave_createcont_box = toga.Box()
        box_createcont = toga.Box()

        id_createcont_input = toga.TextInput()
        clave_createcont_input = toga.TextInput()

        id_createcont_label = toga.Label('ID contacto: ')
        clave_createcont_label = toga.Label('Clave: ')

        createcont_button = toga.Button('Crear contacto')

        id_createcont_box.add(id_createcont_input)
        id_createcont_box.add(id_createcont_label)

        clave_createcont_box.add(clave_createcont_input)
        clave_createcont_box.add(clave_createcont_label)

        box_createcont.add(id_createcont_box)
        box_createcont.add(clave_createcont_box)
        box_createcont.add(createcont_button)

        return box_createcont
