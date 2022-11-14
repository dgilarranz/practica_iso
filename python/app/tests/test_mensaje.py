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
