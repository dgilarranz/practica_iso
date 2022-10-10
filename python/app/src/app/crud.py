import sqlite3 as sql

def createDB (): 
    conn = sql.connect("usuario.db") 
    conn.commit()
    conn.close()

def createTable ():
    conn = sql.connect("usuario.db")
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    cursor.execute( 
        """CREATE TABLE usuario ( 
            hash blob,
            pub_key blob,
            priv_key blob
            )"""
    )
    conn.commit()
    conn.close()

def insertRow(hash,pub_key,priv_key): #meter una fila
    conn = sql.connect("usuario.db")
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"INSERT INTO usuario VALUES ('{hash}', {pub_key}, {priv_key})"
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
        