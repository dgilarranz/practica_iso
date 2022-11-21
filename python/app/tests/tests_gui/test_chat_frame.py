from app.gui.chat_frame import ChatFrame
from app.observer import Observer
from app.factories.chat_factory import ChatFactory
from app.config_manager import ConfigManager
from app.sockets import ConnectionManager
from app.mensaje import Mensaje
from app.setup import inicializar_usuario
from unittest.mock import patch

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
    ConfigManager().user = inicializar_usuario()
    chat = ChatFactory().create_new_chat()
    mensaje = Mensaje("Prueba", chat.id_chat, "blabla")
    chat.messages.append(mensaje)
    chat_frame = ChatFrame(chat)
    
    with patch.object(chat_frame, "add_message") as mock_add_message:
        chat_frame.update()
        mock_add_message.assert_called_once()

def test_chat_frame_adds_message_with_correct_content_when_notified():
    ConfigManager().connection_manager = ConnectionManager()
    ConfigManager().user = inicializar_usuario()
    chat = ChatFactory().create_new_chat()
    mensaje = Mensaje("Prueba", chat.id_chat, "blabla")
    chat.messages.append(mensaje)
    chat_frame = ChatFrame(chat)
    
    with patch.object(chat_frame, "add_message") as mock_add_message:
        chat_frame.update()
        mock_add_message.assert_called_with(mensaje, mensaje.id_sender)

def test_chat_frame_adds_all_messages_with_correct_content_when_notified():
    ConfigManager().connection_manager = ConnectionManager()
    ConfigManager().user = inicializar_usuario()
    chat = ChatFactory().create_new_chat()
    mensaje_1 = Mensaje("Soy el mensaje 1", chat.id_chat, "A mí me envía Pepe")
    mensaje_2 = Mensaje("Soy el mensaje 2", chat.id_chat, "A mí me envía Pepas")
    chat.messages.append(mensaje_1)
    chat.messages.append(mensaje_2)
    chat_frame = ChatFrame(chat)
    
    with patch.object(chat_frame, "add_message") as mock_add_message:
        chat_frame.update()
        mock_add_message.assert_called_with(mensaje_2, mensaje_2.id_sender)
