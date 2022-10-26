import toga
from toga.style import Pack
from toga.style.pack import COLUMN

class NewChatFrame(toga.Window):
    def __init__(self) -> None:
        super().__init__(title="Nuevo chat")
        main_box = toga.Box(id="main_box", style=Pack(direction=COLUMN, background_color="#155757"))

        container = toga.OptionContainer()
        create_chat = self.crearChat()
        join_chat = self.unirseChat()

        container.add('Crear', create_chat)
        container.add('Unirse', join_chat)
        
        main_box.add(container)
        self.content = main_box
        self.content.refresh()

    def crearChat(self) -> toga.Box:
        id_create_box = toga.Box()
        clave_create_box = toga.Box()
        box_create = toga.Box()

        id_create_input = toga.TextInput(readonly=True)
        clave_create_input = toga.TextInput(readonly=True)

        id_create_label = toga.Label('ID: ')
        clave_create_label = toga.Label('Clave: ')

        create_button = toga.Button('Crear chat')

        id_create_box.add(id_create_input)
        id_create_box.add(id_create_label)

        clave_create_box.add(clave_create_input)
        clave_create_box.add(clave_create_label)

        box_create.add(id_create_box)
        box_create.add(clave_create_box)
        box_create.add(create_button)

        return box_create

    def unirseChat(self) -> toga.Box:
        id_join_box = toga.Box()
        clave_join_box = toga.Box()
        box_join = toga.Box()

        id_join_input = toga.TextInput()
        clave_join_input = toga.TextInput()

        id_join_label = toga.Label('ID: ')
        clave_join_label = toga.Label('Clave: ')

        join_button = toga.Button('Unirse al chat')

        id_join_box.add(id_join_input)
        id_join_box.add(id_join_label)

        clave_join_box.add(clave_join_input)
        clave_join_box.add(clave_join_label)

        box_join.add(id_join_box)
        box_join.add(clave_join_box)
        box_join.add(join_button)

        return box_join