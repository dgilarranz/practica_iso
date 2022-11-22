from importlib.resources import path
import resource
import sqlite3 as sql
from xml.dom.minidom import CharacterData
#from app.setup import inicializar_usuario
import pytest
from app.crud import createDB
from unittest.mock import patch
import os
from app.contacto import Contacto
from app.crud import insertar_contacto
from app.crud import leer_contacto
from app.crud import actualizar_contacto
from app.crud import borrar_contacto
from app.chat import Chat
from app.crud import insertar_chat
from app.crud import leer_chat
from app.crud import actualizar_chat
from app.crud import borrar_chat
from app.mensaje import Mensaje
from app.crud import insertar_mensaje
from app.crud import leer_mensaje
from app.crud import actualizar_mensaje
from app.crud import borrar_mensaje
from app.cyphersuite import cifrar_mensaje
from app.cyphersuite import descifrar_mensaje
from app.cyphersuite import hash_to_string
from app.cyphersuite import string_to_hash
from app.cyphersuite import priv_key_to_string
from app.cyphersuite import string_to_priv_key
from app.cyphersuite import pub_key_to_string
from app.cyphersuite import string_to_pub_key
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from app.config_manager import ConfigManager
from app.sockets import ConnectionManager

from app.crud import actualizar_chat

@pytest.fixture(scope="session", autouse = True)
def crear_datos_para_test():
    conn = sql.connect("resources/pruebas.db")
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    cursor.execute("CREATE TABLE Contacto(hash text, pub_key text, ip text, PRIMARY KEY (hash))")
    cursor.execute("CREATE TABLE Chat(id_chat text, key text, PRIMARY KEY (id_chat))")
    cursor.execute("CREATE TABLE Mensaje(mensaje_cifrado text, PRIMARY KEY (mensaje_cifrado))")

    #consultas para Contacto
    cursor.execute("INSERT INTO Contacto VALUES ('contacto_prueba', 'pub_key_prueba','1.1.1.1')")
    #cursor.execute("UPDATE Contacto SET ip = '2.2.2.2' WHERE ip like '1.1.1.1'")
    #cursor.execute("DELETE FROM Contacto WHERE ip like '1.1.1.1'")
    #consultas para chat
    cursor.execute("INSERT INTO Chat VALUES ('id_chat_prueba','key_prueba')")
    #cursor.execute("UPDATE Chat SET id_chat = '1'")
    #cursor.execute("DELETE FROM Chat WHERE id_chat = 'id_chat_prueba'")
    #consultas para mensaje
    #cursor.execute("INSERT INTO Mensaje values ('")
    print("ping")
    conn.commit()
    conn.close()
    yield
    os.remove("resources/pruebas.db")

@pytest.fixture
def crear_chat() -> Chat:
    # Creamos un chat de prueba
    ConfigManager.connection_manager = ConnectionManager()
    chat_hash = hashes.Hash(hashes.SHA256())
    chat_hash = chat_hash.finalize()
    key = Fernet.generate_key()
    return Chat(chat_hash, key)

@pytest.fixture
def crear_mensaje(crear_chat:Chat) -> Mensaje:
    chat = crear_chat
    return Mensaje('texto_prueba', hash_to_string(chat.id_chat), "sender_prueba")

@patch("app.crud.RUTA_BBDD", "resources/pruebaCreacion.db")
def test_crear_base_de_datos():
    createDB()
    conn = sql.connect("resources/pruebaCreacion.db") 
    consulta = f"SELECT count (*) from sqlite_master WHERE type = 'table';"
    cursor = conn.cursor()
    cursor.execute(consulta)
    resultado = cursor.fetchone()
    #print(resultado)
    assert resultado[0] == 4
    os.remove("resources/pruebaCreacion.db")

##TEST CONTACTO

@patch("app.crud.RUTA_BBDD", "resources/pruebas.db")
def no_test_insertar_contacto():
    contacto = Contacto(k_pub="kpub_prueba",direccion_ip="IP_prueba",hash="hash_prueba")
    insertar_contacto(contacto)
    conn = sql.connect("resources/pruebas.db") 
    consulta = f"SELECT ip from Contacto WHERE hash = 'hash_prueba';"
    cursor = conn.cursor()
    cursor.execute(consulta)
    resultado = cursor.fetchone()
    assert resultado[0] == contacto.direccion_ip

@patch("app.crud.RUTA_BBDD", "resources/pruebas.db")
def test_leer_contacto():
    contacto = leer_contacto('contacto_prueba')
    assert contacto.direccion_ip == '1.1.1.1'

@patch("app.crud.RUTA_BBDD", "resources/pruebas.db")
def test_actualizar_contacto():
    contacto = Contacto(k_pub="kpub_prueba",direccion_ip="IP_prueba",hash="contacto_prueba")
    actualizar_contacto(contacto, '2.2.2.2') #definir la funcion en la clase crud
    conn = sql.connect("resources/pruebas.db") 
    consulta = f"SELECT ip from Contacto WHERE hash = 'contacto_prueba';"
    cursor = conn.cursor()
    cursor.execute(consulta)
    resultado = cursor.fetchone()
    assert resultado[0] == '2.2.2.2'

@patch("app.crud.RUTA_BBDD", "resources/pruebas.db")
def no_test_borrar_contacto():
    contacto = Contacto(k_pub="kpub_prueba",direccion_ip="IP_prueba",hash="contacto_prueba")
    borrar_contacto(contacto) #definir la funcion en la clase crud
    conn = sql.connect("resources/pruebas.db") 
    consulta = f"SELECT ip from Contacto WHERE hash = 'contacto_prueba';"
    cursor = conn.cursor()
    cursor.execute(consulta)
    resultado = cursor.fetchone()
    assert resultado[0] == []

## TEST CHAT

@patch("app.crud.RUTA_BBDD", "resources/pruebas.db")
def test_insertar_chat(crear_chat: Chat):
    chat = crear_chat
    insertar_chat(chat)
    conn = sql.connect("resources/pruebas.db")
    consulta = f"SELECT key from Chat WHERE id_chat = '{hash_to_string(chat.id_chat)}';"
    cursor=conn.cursor()
    cursor.execute(consulta)
    resultado=cursor.fetchone()
    assert resultado[0] == hash_to_string(chat.key)

@patch("app.crud.RUTA_BBDD", "resources/pruebas.db")
def test_leer_chat(crear_chat: Chat):
    chat=crear_chat
    assert leer_chat(hash_to_string(chat.id_chat)).id_chat == chat.id_chat    

@patch("app.crud.RUTA_BBDD", "resources/pruebas.db")
def test_actualizar_chat(crear_chat: Chat):
    chat = crear_chat
    actualizar_chat(hash_to_string(chat.id_chat))
    conn = sql.connect("resources/pruebas.db") 
    consulta = f"SELECT id_chat from Chat WHERE id_chat = '1';"
    cursor = conn.cursor()
    cursor.execute(consulta)
    resultado = cursor.fetchone()
    assert resultado[0] == '1'

@patch("app.crud.RUTA_BBDD", "resources/pruebas.db")
def test_borrar_chat(crear_chat: Chat):
    chat = crear_chat
    borrar_chat(chat)
    conn = sql.connect("resources/pruebas.db") 
    consulta = f"SELECT key from Chat WHERE id_chat = '{hash_to_string(chat.id_chat)}';"
    cursor = conn.cursor()
    cursor.execute(consulta)
    resultado = cursor.fetchone()
    assert resultado is None

##TEST MENSAJE

@patch("app.crud.RUTA_BBDD", "resources/pruebas.db")
def test_insertar_mensaje(crear_chat: Chat):
    chat = crear_chat
    user = inicializar_usuario()
    mensaje = Mensaje('texto_prueba', hash_to_string(chat.id_chat), "id_sender")
    mensaje.id_mensaje = b'id_mensaje'.decode('utf-8')
    mensaje_cifrado = hash_to_string(Fernet(chat.key).encrypt(mensaje.to_json().encode("utf-8")))
    insertar_mensaje(mensaje_cifrado)
    conn = sql.connect("resources/pruebas.db")
    consulta = f"SELECT mensaje_cifrado from Mensaje;"
    cursor=conn.cursor()
    cursor.execute(consulta)
    resultado=cursor.fetchone()
    assert resultado[0] == mensaje_cifrado

@patch("app.crud.RUTA_BBDD", "resources/pruebas.db")
def no_test_leer_mensaje(crear_mensaje: Mensaje):
    mensaje = crear_mensaje
    assert leer_mensaje(hash_to_string(mensaje.id_mensaje)).id_mensaje == mensaje.id_mensaje

@patch("app.crud.RUTA_BBDD", "resources/pruebas.db")
def no_test_actualizar_mensaje(crear_mensaje: Mensaje):
    mensaje = crear_mensaje
    actualizar_mensaje(mensaje)
    conn = sql.connect("resources/prueba.db")
    consulta = f"SELECT texto from Mensaje WHERE id_mensaje = '{hash_to_string(mensaje.id_mensaje)}';"
    cursor = conn.cursor()
    cursor.execute(consulta)
    resultado = consulta.fetchone()
    assert resultado[0] == ['prueba'] 

@patch("app.crud.RUTA_BBDD", "resources/pruebas.db")
def no_test_borrar_mensaje(crear_mensaje: Mensaje):
    mensaje = crear_mensaje
    borrar_mensaje(mensaje)
    conn = sql.connect("resources/prueba.db")
    consulta = f"SELECT texto from Mensaje WHERE id_mensaje = '{hash_to_string(mensaje.id_mensaje)}';"
    cursor = conn.cursor()
    cursor.execute(consulta)
    resultado = consulta.fetchone()
    assert resultado[0] == [] 




















    

