import binascii
from app.setup import inicializar_usuario
from app.file_manager import guardar_usuario
import json

def test_guardar_usuario():
    usuario = inicializar_usuario()
    guardar_usuario(usuario) #falta 
    f = open('resources/config.json', 'r') #abre un fichero en modo lectura
    contenido = json.load(f)
    assert contenido['hash'] == binascii.hexlify(usuario.hash).decode('UTF-8')
