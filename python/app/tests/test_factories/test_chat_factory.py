from app.chat import Chat
from app.crud import leer_chat
from app.cyphersuite import hash_to_string
from app.factories.chat_factory import ChatFactory

def test_creation_of_new_chat_not_in_database():
    chat = ChatFactory().create_chat()
    id_chat = hash_to_string(chat.id_chat)
    db_chat = leer_chat(id_chat)
    assert chat.id_chat == db_chat.id_chat

def test_another_creation_of_new_chat_not_in_database():
    chat = ChatFactory().create_chat()
    id_chat = hash_to_string(chat.id_chat)
    db_chat = leer_chat(id_chat)
    assert chat is not None and db_chat is not None and chat.id_chat == db_chat.id_chat

def test_chats_have_different_ids():
    factory = ChatFactory()
    chat_1 = factory.create_chat()
    chat_2 = factory.create_chat()
    assert chat_1.id_chat != chat_2.id_chat