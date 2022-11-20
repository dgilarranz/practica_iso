from app.gui.chat_frame import ChatFrame
from app.observer import Observer
from app.factories.chat_factory import ChatFactory
from app.config_manager import ConfigManager
from app.sockets import ConnectionManager

def test_chat_frame_is_observer():
    ConfigManager().connection_manager = ConnectionManager()
    chat = ChatFactory().create_new_chat()
    chat_frame = ChatFrame(chat)
    assert isinstance(chat_frame, Observer)