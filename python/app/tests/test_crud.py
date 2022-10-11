from importlib.resources import path
import resource
import sqlite3 as sql
import pytest
from app.crud import createDB
from unittest.mock import patch
import os
from app.contacto import Contacto
from app.crud import insertar_contacto
from app.crud import leer_contacto

@pytest.fixture(scope="session", autouse = True)
def crear_datos_para_test():
    conn = sql.connect("resources/pruebas.db") #cambiar nombre de la bbdd con el nombre de cristina
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    cursor.execute("CREATE TABLE Contacto(hash text, pub_key text, ip text, PRIMARY KEY (hash))")
    cursor.execute("CREATE TABLE Chat(id_chat text, PRIMARY KEY (id_chat))")
    cursor.execute("CREATE TABLE Mensaje(id_mensaje text, texto text, id_chat text, TTL text, Timestamp text, PRIMARY KEY (id_mensaje), FOREIGN KEY (id_chat) REFERENCES Chat(id_chat))")

    cursor.execute("INSERT INTO Contacto VALUES ('contacto_prueba', 'pub_key_prueba','1.1.1.1')")
    #hacer para chat y mensaje
    print("ping")
    conn.commit()
    conn.close()
    yield
    os.remove("resources/pruebas.db")



@patch("app.crud.RUTA_BBDD", "resources/pruebaCreacion.db")
def test_crear_base_de_datos():
    createDB()
    conn = sql.connect("resources/pruebaCreacion.db") 
    consulta = f"SELECT count (*) from sqlite_master WHERE type = 'table';"
    cursor = conn.cursor()
    cursor.execute(consulta)
    resultado = cursor.fetchone()
    #print(resultado)
    assert resultado[0] == 3
    os.remove("resources/pruebaCreacion.db")

@patch("app.crud.RUTA_BBDD", "resources/pruebas.db")
def test_insertar_contacto():
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




    

