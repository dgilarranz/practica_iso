from app.gui.chat_frame import ChatFrame
from app.observer import Observer
from app.factories.chat_factory import ChatFactory
from app.config_manager import ConfigManager
from app.sockets import ConnectionManager
from app.mensaje import Mensaje
from app.file_manager import leer_usuario
from unittest.mock import patch
from app.gui.money_frame import MoneyFrame
import toga
import pytest
import pytest_asyncio

def test_chat_frame_is_observer():
    ConfigManager().connection_manager = ConnectionManager()
    chat = ChatFactory().create_new_chat()
    chat_frame = ChatFrame(chat)
    assert isinstance(chat_frame, Observer)

def test_chat_frame_is_subscribed_to_chat():
    ConfigManager().connection_manager = ConnectionManager()
    chat = ChatFactory().create_new_chat()
    chat_frame = ChatFrame(chat)
    assert chat_frame in chat.subscribers

def test_chat_frame_adds_message_to_content_when_notified():
    ConfigManager().connection_manager = ConnectionManager()
    ConfigManager().user = leer_usuario()
    chat = ChatFactory().create_new_chat()
    mensaje = Mensaje("Prueba", chat.id_chat, "blabla")
    chat.messages.append(mensaje)
    chat_frame = ChatFrame(chat)
    
    with patch.object(chat_frame, "add_message") as mock_add_message:
        chat_frame.update()
        mock_add_message.assert_called_once()

def test_chat_frame_adds_message_with_correct_content_when_notified():
    ConfigManager().connection_manager = ConnectionManager()
    ConfigManager().user = leer_usuario()
    chat = ChatFactory().create_new_chat()
    mensaje = Mensaje("Prueba", chat.id_chat, "blabla")
    chat.messages.append(mensaje)
    chat_frame = ChatFrame(chat)
    
    with patch.object(chat_frame, "add_message") as mock_add_message:
        chat_frame.update()
        mock_add_message.assert_called_with(mensaje.texto, mensaje.id_sender)

def test_chat_frame_adds_all_messages_with_correct_content_when_notified():
    ConfigManager().connection_manager = ConnectionManager()
    ConfigManager().user = leer_usuario()
    chat = ChatFactory().create_new_chat()
    mensaje_1 = Mensaje("Soy el mensaje 1", chat.id_chat, "A mí me envía Pepe")
    mensaje_2 = Mensaje("Soy el mensaje 2", chat.id_chat, "A mí me envía Pepas")
    chat.messages.append(mensaje_1)
    chat.messages.append(mensaje_2)
    chat_frame = ChatFrame(chat)
    
    with patch.object(chat_frame, "add_message") as mock_add_message:
        chat_frame.update()
        mock_add_message.assert_called_with(mensaje_2.texto, mensaje_2.id_sender)

def test_chat_frame_adds_refeshes_content_when_notified():
    ConfigManager().connection_manager = ConnectionManager()
    ConfigManager().user = leer_usuario()
    chat = ChatFactory().create_new_chat()
    chat_frame = ChatFrame(chat)
    
    with patch.object(chat_frame.content, "refresh") as mock_refresh:
        chat_frame.update()
        mock_refresh.assert_called_once()

def test_chat_frame_adds_errases_previous_content_when_notified():
    ConfigManager().connection_manager = ConnectionManager()
    ConfigManager().user = leer_usuario()
    chat = ChatFactory().create_new_chat()
    mensaje_1 = Mensaje("Prueba", chat.id_chat, "blabla")
    chat.messages.append(mensaje_1)
    chat_frame = ChatFrame(chat)

    mensaje_2 = Mensaje("Probamos correcto funcionamiento", chat.id_chat, "blabla")
    chat.messages.append(mensaje_2)
    chat.notify()

    assert len(chat_frame.message_container.children) == 2

@patch("asyncio.create_task")
@patch("app.crud.insertar_mensaje")
@pytest.mark.asyncio
async def test_chat_frame_clears_input_text_after_send(mock_create_task, mock_insertar_mensaje):
    ConfigManager().connection_manager = ConnectionManager()
    ConfigManager().user = leer_usuario()

    chat = ChatFactory().create_new_chat()
    mensaje_1 = Mensaje("Prueba", chat.id_chat, "blabla")
    chat.messages.append(mensaje_1)

    chat_frame = ChatFrame(chat)
    chat_frame.message_input.value = "Mensaje Blablabla ... Fin Mensaje"
    await chat_frame.send_message(None)

    assert chat_frame.message_input.value == ""

def test_send_crypto_opens_money_window():
    app = toga.App()
    chat = ChatFactory().create_new_chat()
    chat_frame = ChatFrame(chat)
    app.windows.add(chat_frame)

    with patch("app.gui.money_frame.MoneyFrame.show") as mock_show:
        chat_frame.send_crypto(None)
        mock_show.assert_called_once()

def test_money_frame_added_to_windows():
    app = toga.App()
    chat = ChatFactory().create_new_chat()
    chat_frame = ChatFrame(chat)
    app.windows.add(chat_frame)
    
    chat_frame.send_crypto(None)

    money_window = None
    for window in app.windows:
        if isinstance(window, MoneyFrame):
            money_window = window
            break

    assert money_window is not None