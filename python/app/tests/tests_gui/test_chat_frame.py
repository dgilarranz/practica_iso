from app.gui.chat_frame import ChatFrame
from app.observer import Observer
from app.factories.chat_factory import ChatFactory
from app.config_manager import ConfigManager
from app.sockets import ConnectionManager
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