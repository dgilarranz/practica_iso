from src.app.chat import Chat
from src.app.contacto import Contacto
import pytest
# poetry run pytest test_chat.py
def test01_crearChat():
    assert Chat(00)

def test02_obtenerIdChat():
    chat= Chat(1)
    assert chat.getID_Chat()==1

def test03_ceroMiembrosAlCrearChat():
    chat = Chat(1)
    assert len(chat.getMiembros())==0

def test04_addMiembros():
    chat = Chat(1)
    #falta añadir miembros, pero como nose si tiene alias y tal
    #pregunto y lo añado
    pass

