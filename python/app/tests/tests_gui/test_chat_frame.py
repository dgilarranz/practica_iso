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

def test_chat_frame_refreshes_content_when_notified():
    ConfigManager().connection_manager = ConnectionManager()
    ConfigManager().user = inicializar_usuario()
    chat = ChatFactory().create_new_chat()
    mensaje = Mensaje("Prueba", chat.id_chat, "blabla")
    chat.messages.append(mensaje)
    chat_frame = ChatFrame(chat)
    
    with patch.object(chat_frame, "add_message") as mock_add_message:
        chat_frame.update()
        mock_add_message.assert_called_once()
