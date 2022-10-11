import sqlite3 as sql
from app.contacto import Contacto


RUTA_BBDD = "resources/database.db"
CONSULTAS_CREATE = [
    "CREATE TABLE Contacto(hash text, pub_key text, ip text, PRIMARY KEY (hash))",
    "CREATE TABLE Chat(id_chat text, PRIMARY KEY (id_chat))",
    """
        CREATE TABLE Mensaje(id_mensaje text, texto text, id_chat text, TTL text, Timestamp text, 
        PRIMARY KEY (id_mensaje), FOREIGN KEY (id_chat) REFERENCES Chat(id_chat))
    """
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
    instruccion = f"INSERT INTO Contacto VALUES ('{contacto.hash}', {contacto.k_pub}, {contacto.direccion_ip})"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def readRows (): #leer filas 
    conn = sql.connect("usuario.db")
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"SELECT * from  usuario"
    cursor.execute(instruccion)
    datos = cursor.fetchall() #nos devuelve todos los datos seleccionados
    conn.commit()
    conn.close()
    print(datos)

def insertRows (list): #meter varias filas
    conn = sql.connect("usuario.db")
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"INSERT INTO usuario VALUES (?,?)"
    cursor.executemany(instruccion,list) #utilizamos esta funcion porque vamos a insertar varios
    conn.commit()
    conn.close()
def readOrdered (field) : #leer en orden
    conn = sql.connect("usuario.db")
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"SELECT * from  usuario ORDER BY {field} DESC"
    cursor.execute(instruccion)
    datos = cursor.fetchall() #nos devuelve todos los datos seleccionados
    conn.commit()
    conn.close()
    print(datos)

def search (): #hacer consultas
    conn = sql.connect("usuario.db")
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"SELECT * from  usuario WHERE hash = ''" 
    cursor.execute(instruccion)
    datos = cursor.fetchall() #nos devuelve todos los datos seleccionados
    conn.commit()
    conn.close()
    print(datos)

def updateFields(): #modificar
    conn = sql.connect("usuario.db")
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"UPDATE usuario SET hash = ? WHERE priv_key like '')"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def deleteRow(): #borrar filas
    conn = sql.connect("usuario.db")
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"DELETE FROM usuario WHERE hash = ''" #cambiar nombre por cualquier valor de la tabla
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
        