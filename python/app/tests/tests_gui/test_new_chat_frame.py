from app.gui.new_chat_frame import NewChatFrame, KeyNotSuppliedException, IdNotSuppliedException
from app.crud import leer_chat, borrar_chat
from app.cyphersuite import hash_to_string
from app.factories.chat_factory import ChatFactory
from app.config_manager import ConfigManager
from app.sockets import ConnectionManager
from unittest.mock import patch
import pytest
import sqlite3 as sql
import os
import toga
from app.gui.main_frame import MainFrame

TEST_DB = "resources/test.db"

@pytest.fixture(scope="function", autouse = True)
def crear_base_datos_para_tests():
    ConfigManager().connection_manager = ConnectionManager()
    try:
        conn = sql.connect(TEST_DB)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE Chat(id_chat text, key text, PRIMARY KEY (id_chat))")
        conn.commit()
        conn.close()
    except sql.OperationalError:
        pass
    yield
    try:
        os.remove(TEST_DB)
    except FileNotFoundError:
        pass

@patch("app.crud.RUTA_BBDD", TEST_DB)
def test_crear_chat_nuevo():
    # Creamos una app con su MainFrame
    app = toga.App()
    app.main_window = MainFrame("", "", [])

    # Creamos un chat
    frame = NewChatFrame()
    app.windows.add(frame)
    frame.create_new_chat(None)

    # Comprobamos que se ha guardado el chat en BBDD y se ha actualizado la ventana
    chat_id = frame.id_create_input.value
    chat_key = frame.clave_create_input.value
    chat = leer_chat(chat_id)

    assert hash_to_string(chat.id_chat) == chat_id and hash_to_string(chat.key) == chat_key

@patch("app.crud.RUTA_BBDD", TEST_DB)
def test_annadir_chat_usando_valores():
    # Creamos un chat y lo borramos de la BBDD para evitar problemas
    chat = ChatFactory().produce()
    chat_id = hash_to_string(chat.id_chat)
    chat_key = hash_to_string(chat.key)
    borrar_chat(chat_id)
    

    # Simulamos la entrada del usuario
    frame = NewChatFrame()
    app = toga.App()
    app.windows.add(frame)
    frame.clave_join_input.value = chat_key
    frame.id_join_input.value = chat_id

    # Añadimos el chat
    frame.join_chat(None)
    db_chat = leer_chat(chat_id)

    # Verificamos que el chat se ha añadido correctamente
    assert hash_to_string(db_chat.id_chat) == chat_id and hash_to_string(db_chat.key) == chat_key

@patch("app.crud.RUTA_BBDD", TEST_DB)
def test_error_si_no_se_introduce_clave():
    chat = ChatFactory().produce()
    chat_id = hash_to_string(chat.id_chat)
    borrar_chat(chat_id)

    frame = NewChatFrame()
    app = toga.App()
    app.windows.add(frame)
    frame.id_join_input.value = chat_id

    with pytest.raises(KeyNotSuppliedException):
        frame.join_chat(None)

@patch("app.crud.RUTA_BBDD", TEST_DB)
def test_error_si_no_se_introduce_id():
    chat = ChatFactory().produce()
    chat_key = hash_to_string(chat.key)
    chat_id = hash_to_string(chat.id_chat)
    borrar_chat(chat_id)

    frame = NewChatFrame()
    app = toga.App()
    app.windows.add(frame)
    frame.clave_join_input.value = chat_key

    with pytest.raises(IdNotSuppliedException):
        frame.join_chat(None)

@patch("app.crud.RUTA_BBDD", TEST_DB)
def test_crear_chat_actualiza_interfaz():
    # Creamos una app con su MainFrame
    app = toga.App()
    app.main_window = MainFrame("", "", [])

    # Creamos un chat
    frame = NewChatFrame()
    app.windows.add(frame)

    # Comprobamos que se ha actualiza la interfaz
    with patch.object(app.main_window, "add_new_chat") as mock_add_chat:
        frame.create_new_chat(None)
        mock_add_chat.assert_called_once()

@patch("app.crud.RUTA_BBDD", TEST_DB)
@patch("app.factories.chat_factory.ChatFactory.produce")
def test_unirse_a_chat_cierra_la_ventana(mock_produce):
    # Creamos una app con su MainFrame
    app = toga.App()
    app.main_window = MainFrame("", "", [])

    # Creamos un chat
    frame = NewChatFrame()
    app.windows.add(frame)

    # Comprobamos que se ha actualiza la interfaz
    with patch.object(frame, "close") as mock_close:
        frame.id_join_input.value = "asdf"
        frame.clave_join_input.value = "asdf"
        frame.join_chat(None)
        mock_close.assert_called_once()