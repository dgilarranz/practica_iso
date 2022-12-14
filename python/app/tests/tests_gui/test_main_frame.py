from app.gui.main_frame import MainFrame
from app.crud import leer_chat
from app.factories.chat_factory import ChatFactory
from app.config_manager import ConfigManager
from app.sockets import ConnectionManager
from app.cyphersuite import hash_to_string
from unittest.mock import patch
from app.gui.app import MessageApp
import toga
import sqlite3 as sql
import os
import pytest

TEST_DB = "resources/test.db"

@pytest.fixture(scope="function", autouse=True)
def crear_base_datos_para_tests():
    conn = sql.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE Chat(id_chat text, key text, PRIMARY KEY (id_chat))")
    conn.commit()
    conn.close()
    yield
    os.remove(TEST_DB)

def test_main_frame_has_map_for_delete_chat_buttons():
    mf = MainFrame("", "", [])
    assert isinstance(mf.delete_btn_map, dict)

def test_chat_has_delete_method():
    mf = MainFrame("", "", [])
    assert callable(mf.delete_chat)

@patch("app.crud.RUTA_BBDD", TEST_DB)
def test_delete_chat_deletes_chat():
    ConfigManager().connection_manager = ConnectionManager()
    chat = ChatFactory().produce()
    id_chat = hash_to_string(chat.id_chat)
    mf = MainFrame("", "", [chat])

    delete_button = toga.Widget(id="id_prueba")
    mf.delete_btn_map[delete_button.id] = chat
    mf.delete_chat(delete_button)

    with pytest.raises(TypeError):
        leer_chat(id_chat) is None

@patch("app.crud.RUTA_BBDD", TEST_DB)
def test_window_is_updated_after_delete():
    ConfigManager().connection_manager = ConnectionManager()
    chat = ChatFactory().produce()
    id_chat = hash_to_string(chat.id_chat)
    mf = MainFrame("", "", [chat])

    delete_button = toga.Widget(id="id_prueba")
    mf.delete_btn_map[delete_button.id] = chat
    
    with patch.object(mf.content, "refresh") as refresh_mock:
        mf.delete_chat(delete_button)
        refresh_mock.assert_called_once()

@patch("app.crud.RUTA_BBDD", TEST_DB)
def test_chat_box_is_removed_after_delete():
    ConfigManager().connection_manager = ConnectionManager()
    chat = ChatFactory().produce()
    id_chat = hash_to_string(chat.id_chat)
    mf = MainFrame("", "", [chat])

    delete_button = toga.Widget(id="id_prueba")
    mf.delete_btn_map[delete_button.id] = chat

    chat_box = list(filter(lambda child: child.id == f"chat_{id_chat}_box", mf.chats_box.children))[0]

    
    with patch.object(mf.chats_box, "remove") as remove_mock:
        mf.delete_chat(delete_button)
        remove_mock.assert_called_once_with(chat_box)

def test_main_frame_has_function_for_adding_a_new_chat_box():
    mf = MainFrame("", "", [])
    assert callable(mf.add_new_chat)

@patch("app.crud.RUTA_BBDD", TEST_DB)
def test_new_chat_box_receives_a_chat():
    ConfigManager().connection_manager = ConnectionManager()
    chat = ChatFactory().produce()
    mf = MainFrame("", "", [])
    mf.add_new_chat(chat)

@patch("app.crud.RUTA_BBDD", TEST_DB)
def test_new_chat_box_creates_a_widget_for_the_chat():
    ConfigManager().connection_manager = ConnectionManager()
    chat = ChatFactory().produce()
    mf = MainFrame("", "", [])

    widget = mf.create_chat_widget(chat) 
    with patch.object(mf, "create_chat_widget") as mock_create_widget:
        mock_create_widget.return_value = widget
        mf.add_new_chat(chat)
        mock_create_widget.assert_called_once_with(chat)

@patch("app.crud.RUTA_BBDD", TEST_DB)
def test_new_chat_box_adds_the_widget_to_window():
    ConfigManager().connection_manager = ConnectionManager()
    chat = ChatFactory().produce()
    id_chat = hash_to_string(chat.id_chat)

    mf = MainFrame("", "", [])
    mf.add_new_chat(chat)

    chat_box = None
    for box in mf.chats_box.children:
        if box.id == f"chat_{id_chat}_box":
            chat_box = box
    assert chat_box is not None
