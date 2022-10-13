from ast import Str
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


RUTA_BBDD = "resources/database.db"
CONSULTAS_CREATE = [
    "CREATE TABLE Contacto(hash text, pub_key text, ip text, PRIMARY KEY (hash))",
    "CREATE TABLE Chat(id_chat text, PRIMARY KEY (id_chat))",
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

def insertar_contacto(contacto): #meter una fila
    conn = sql.connect(RUTA_BBDD)
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"INSERT INTO Contacto VALUES ('{contacto.hash}', '{contacto.k_pub}', '{contacto.direccion_ip}')"
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
    return Contacto(hash=datos[0],k_pub=datos[1],direccion_ip=datos[2])

def insertar_chat(chat:Chat): #meter varias filas
    conn = sql.connect(RUTA_BBDD)
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"INSERT INTO Chat VALUES ('{hash_to_string(chat.id_chat)}', '{pub_key_to_string(chat.pub_key)}', '{priv_key_to_string(chat.priv_key)}')"
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
    return Chat(id_chat=string_to_hash(datos[0]),pub_key= string_to_pub_key(datos[1]), priv_key= string_to_priv_key(datos[2]))

def insertar_mensaje(mensaje:str): #modificar
    conn = sql.connect(RUTA_BBDD)
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"INSERT INTO Mensaje VALUES ('{mensaje}')"
    cursor.execute(instruccion)
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