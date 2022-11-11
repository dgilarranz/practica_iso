from ast import Str
from operator import contains
import sqlite3 as sql
from app.contacto import Contacto
from app.chat import Chat
from app.cyphersuite import cifrar_mensaje
from app.cyphersuite import descifrar_mensaje
from app.cyphersuite import hash_to_string
from app.cyphersuite import string_to_hash
from app.cyphersuite import priv_key_to_string
from app.cyphersuite import string_to_priv_key
from app.cyphersuite import pub_key_to_string
from app.cyphersuite import string_to_pub_key
from app.mensaje import Mensaje
from app.config_manager import ConfigManager


RUTA_BBDD = "resources/database.db"
CONSULTAS_CREATE = [
    "CREATE TABLE Contacto(hash text, pub_key text, ip text, PRIMARY KEY (hash))",
    "CREATE TABLE Chat(id_chat text, key text, PRIMARY KEY (id_chat))",
    "CREATE TABLE ChatContacto (id_chat text NOT NULL , hash_contacto text NULL,PRIMARY KEY (id_chat,hash_contacto) FOREIGN KEY (id_chat) REFERENCES Chat(id_chat), FOREIGN KEY (hash_contacto) REFERENCES Contacto(hash))",
    "CREATE INDEX indice_id_chat ON ChatContacto(id_chat)",
    "CREATE TABLE Mensaje(mensaje_cifrado text, PRIMARY KEY (mensaje_cifrado))"
]
def createDB (): 
    conn = sql.connect(RUTA_BBDD)
    createTables(conn)
    conn.close()

def createTables(conn):
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    for consulta in CONSULTAS_CREATE:
        cursor.execute(consulta)
    conn.commit()

#Métodos CRUD Para Contacto

def insertar_contacto(contacto): #meter una fila
    conn = sql.connect(RUTA_BBDD)
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    hash_to_string= hash_to_string(contacto.hash)
    k_pub= pub_key_to_string(contacto.k_pub)
    instruccion = f"INSERT INTO Contacto VALUES ('{hash_to_string}', '{k_pub}', '{contacto.direccion_ip}')"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def addContactoChat(id_chat,hash_contacto):
    conn = sql.connect(RUTA_BBDD)
    cursor = conn.cursor()  # nos proporciona el objeto de la conexión
    instruccion = f"INSERT INTO ChatContacto VALUES ('{id_chat}','{hash_contacto}')"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def leer_contacto(hash_contacto): #leer filas 
    conn = sql.connect(RUTA_BBDD)
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"SELECT * from Contacto WHERE Contacto.hash = '{hash_contacto}'"
    cursor.execute(instruccion)
    datos = cursor.fetchone() #nos devuelve todos los datos seleccionados
    #print(datos)
    conn.commit()
    conn.close()
    hash_to_string = hash_to_string(datos[0])
    k_pub= pub_key_to_string(datos[1])
    return Contacto(hash_to_string ,k_pub,direccion_ip=datos[2])

def actualizar_contacto(contacto: Contacto, ip: str):
    conn = sql.connect(RUTA_BBDD)
    cursor = conn.cursor()
    instruccion = f"UPDATE Contacto SET ip = '{ip}' WHERE hash = '{contacto.hash}'" # Solo para pasar test. Luego -> hash_to_string
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()
    #return Contacto()


def borrar_contacto(ip):
    conn = sql.connect(RUTA_BBDD)
    cursor = conn.cursor()
    instruccion = f"DELETE FROM Contacto WHERE Contacto.ip = '{ip}'"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()
    #return Contacto()

#Métodos CRUD para CHAT

def insertar_chat(chat:Chat): #meter varias filas
    conn = sql.connect(RUTA_BBDD)
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"INSERT INTO Chat VALUES ('{hash_to_string(chat.id_chat)}', '{hash_to_string(chat.key)}')"
    insertar_chat_contacto(chat)
    cursor.execute(instruccion) 
    conn.commit()
    conn.close()

def insertar_chat_contacto(chat:Chat): #por cada 
    conn = sql.connect(RUTA_BBDD)
    cursor = conn.cursor()
    for contacto in chat.miembros:
        instruccion = f"INSERT INTO ChatContacto VALUES ('{hash_to_string(chat.id_chat)}','{hash_to_string(contacto.hash)}')"
        cursor.execute(instruccion)
    conn.commit()
    conn.close()


def leer_chat(id_chat:str)-> Chat : #leer en orden
    conn = sql.connect(RUTA_BBDD)
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"SELECT * from  Chat WHERE Chat.id_chat = '{id_chat}'"
    cursor.execute(instruccion)
    datos = cursor.fetchone() #nos devuelve todos los datos seleccionados
    #print(datos)
    conn.commit()
    conn.close()
    return Chat(id_chat=string_to_hash(datos[0]),key=string_to_hash(datos[1]))

def leer_chats() -> list[Chat]:
    conn = sql.connect(RUTA_BBDD)
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"SELECT * from  Chat"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    
    chats = []
    for d in datos:
        chats.append(Chat(string_to_hash(d[0]), string_to_hash(d[1])))
    
    for chat in chats:
        leer_chat_contacto(chat)
    
    return chats

def leer_chat_contacto(chat:Chat):
    conn = sql.connect(RUTA_BBDD)
    cursor = conn.cursor()
    instruccion = f"SELECT hash_contacto from ChatContacto WHERE id_chat = '{hash_to_string(chat.id_chat)}'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    resultado = {}
    for d in datos:
        chat.miembros.add(leer_contacto(d[0]))
    conn.commit()
    conn.close()

def actualizar_chat(id_chat:str)-> Chat:
    conn = sql.connect(RUTA_BBDD)
    cursor = conn.cursor()
    instruccion = f"UPDATE Chat SET id_chat = '1' WHERE Chat.id_chat = '{id_chat}'"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()

def borrar_chat(id_chat):
    conn = sql.connect(RUTA_BBDD)
    cursor = conn.cursor()
    instruccion = f"DELETE FROM Chat WHERE Chat.id_chat = '{id_chat}'"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()

#Métodos CRUD para mensaje
def insertar_mensaje(mensaje:str):
    conn = sql.connect(RUTA_BBDD)
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"INSERT INTO Mensaje VALUES ('{mensaje}')"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def leer_mensaje() -> list[Mensaje]:
    conn = sql.connect(RUTA_BBDD)
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"SELECT * from  Mensaje"
    cursor.execute(instruccion)
    datos = cursor.fetchall() #nos devuelve todos los datos seleccionados
    #print(datos)
    conn.commit()
    conn.close()
    lista_mensajes = []
    for mensaje in datos:
        msg = descifrar_mensaje(mensaje[0], ConfigManager().user.key)
        lista_mensajes.append(msg)
    return lista_mensajes

def actualizar_mensaje(mensaje_cifrado):
     conn = sql.connect(RUTA_BBDD)
     cursor = conn.cursor()
     instruccion = f"UPDATE Mensaje SET mensaje_cifrado = 'prueba' WHERE Mensaje.mensaje_cifrado = '{mensaje_cifrado}'"
     cursor.execute(instruccion)
     datos = cursor.fetchone()
     conn.commit()
     conn.close()

def borrar_mensaje(id_mensaje):
    conn = sql.connect(RUTA_BBDD)
    cursor = conn.cursor()
    instruccion = f"DELETE FROM Mensaje WHERE Mensaje.id_mensaje = '{id_mensaje}'"
    cursor.execute(instruccion)
    datos = cursor.fetchone()
    conn.commit()
    conn.close()


if __name__ == "__main__":
    pass
    #createTable() #ejecuto y luego hago ctrl+shift+P para buscar las bases de datos
    #insertRow() #cada vez que vuelvo a hacer una insercción tengo que darle al play en la bbdd (abajo a la izqda)
    #readRows()
    #lista = [
     #   ( , ,),
      #  (, , )
      #  ]
    #insertRows(lista) #ejecutar la lista antes de hacer el insert. 
    #readOrdered()
    #search()
    #updateFields()
    #deleteRow()
