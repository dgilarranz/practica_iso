from email import message
import json
from app.mensaje import Mensaje
from uuid import UUID

def test_to_json():
    message = Mensaje("text", "id_chat", None)
    json_message = message.to_json()

    assert json.loads(json_message)['texto'] == 'text' 

def test_message_has_uuid():
    message = Mensaje("text", "id_chat", None)
    assert isinstance(message.id_mensaje, UUID)

def test_from_json():
    message = Mensaje("text", "id_chat", None)
    json_message = message.to_json()

    received_message = Mensaje.from_json(json_message)
    assert str(received_message.id_mensaje) == str(message.id_mensaje)

def test_from_json_with_ttl():
    message = Mensaje("text", "id_chat", None)
    message.ttl = 1
    json_message = message.to_json()

    received_message = Mensaje.from_json(json_message)
    assert received_message.ttl == message.ttl

def test_from_json_with_another_ttl():
    message = Mensaje("text", "id_chat", None)
    message.ttl = 2
    json_message = message.to_json()

    received_message = Mensaje.from_json(json_message)
    assert received_message.ttl == message.ttl

def test_from_json_same_text():
    message = Mensaje("texto 1", "id_chat", None)
    json_message = message.to_json()

    received_message = Mensaje.from_json(json_message)
    assert received_message.texto == message.texto

def test_from_json_another_text():
    message = Mensaje("texto 2", "id_chat", None)
    json_message = message.to_json()

    received_message = Mensaje.from_json(json_message)
    assert received_message.texto == message.texto

def test_from_json_same_chat():
    message = Mensaje("texto 1", "id_chat 1", None)
    json_message = message.to_json()

    received_message = Mensaje.from_json(json_message)
    assert received_message.id_chat == message.id_chat

def test_from_json_another_chat():
    message = Mensaje("texto 1", "id_chat 2", None)
    json_message = message.to_json()

    received_message = Mensaje.from_json(json_message)
    assert received_message.id_chat == message.id_chat