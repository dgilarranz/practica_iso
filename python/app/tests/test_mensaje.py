from email import message
import json
from app.mensaje import Mensaje

def test_to_json():
    message = Mensaje("text", "id_chat", None)
    json_message = message.to_json()

    assert json.loads(json_message)['texto'] == 'text' 
