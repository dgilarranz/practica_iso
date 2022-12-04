import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from app.factories.chat_factory import ChatFactory
from app.cyphersuite import hash_to_string

class NewChatFrame(toga.Window):
    def __init__(self) -> None:
        super().__init__(title="Nuevo chat")
        main_box = toga.Box(id="main_box", style=Pack(direction=COLUMN))

        container = toga.OptionContainer()
        create_chat = self.crearChat()
        join_chat = self.unirseChat()

        container.add('Crear', create_chat)
        container.add('Unirse', join_chat)
        
        main_box.add(container)
        self.content = main_box
        self.content.refresh()

    def crearChat(self) -> toga.Box:
        id_create_box = toga.Box(style=Pack(padding=10))
        clave_create_box = toga.Box(style=Pack(padding=10))
        box_create = toga.Box(style=Pack(direction=COLUMN))

        self.id_create_input = toga.TextInput(readonly=True, style=Pack(flex=1))
        self.clave_create_input = toga.TextInput(readonly=True, style=Pack(flex=1))

        id_create_label = toga.Label('ID:', style=Pack(padding_left = 5, padding_right = 50))
        clave_create_label = toga.Label('Clave:', style=Pack(padding_left = 5, padding_right = 10))

        create_button = toga.Button('Crear chat', on_press=self.create_new_chat)

        id_create_box.add(id_create_label)
        id_create_box.add(self.id_create_input)

        clave_create_box.add(clave_create_label)
        clave_create_box.add(self.clave_create_input)

        box_create.add(id_create_box)
        box_create.add(clave_create_box)
        box_create.add(create_button)

        return box_create

    def unirseChat(self) -> toga.Box:
        id_join_box = toga.Box(style=Pack(padding=10))
        clave_join_box = toga.Box(style=Pack(padding=10))
        box_join = toga.Box(style=Pack(direction=COLUMN))

        self.id_join_input = toga.TextInput(style=Pack(flex=1))
        self.clave_join_input = toga.TextInput(style=Pack(flex=1))

        id_join_label = toga.Label('ID:', style=Pack(padding_left = 5, padding_right = 50))
        clave_join_label = toga.Label('Clave:', style=Pack(padding_left = 5, padding_right = 10))

        join_button = toga.Button('Unirse al chat', on_press=self.join_chat)

        id_join_box.add(id_join_label)
        id_join_box.add(self.id_join_input)

        clave_join_box.add(clave_join_label)
        clave_join_box.add(self.clave_join_input)

        box_join.add(id_join_box)
        box_join.add(clave_join_box)
        box_join.add(join_button)

        return box_join

    def create_new_chat(self, widget):
        factory = ChatFactory()
        chat = factory.produce()
        self.id_create_input.value = hash_to_string(chat.id_chat)
        self.clave_create_input.value = hash_to_string(chat.key)
        self.app.main_window.add_new_chat(chat)
        self.close()

    def join_chat(self, widget):
        id_chat = self.id_join_input.value
        key = self.clave_join_input.value

        if key == "":
            raise KeyNotSuppliedException()
        elif id_chat == "":
            raise IdNotSuppliedException()

        factory = ChatFactory(id_chat, key)
        factory.produce()
        self.close()

class KeyNotSuppliedException(Exception):
    pass

class IdNotSuppliedException(Exception):
    pass