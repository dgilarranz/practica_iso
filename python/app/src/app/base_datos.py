import sqlite3 as sql

def createDB (): #de prueba. Hace lo mismo que la de abajo
    conn = sql.connect("hola.db") #cambiar nombre de la bbdd con el nombre de cristina
    conn.commit()
    conn.close()

def createTable ():
    conn = sql.connect("hola.db")
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    cursor.execute( #otra vez depende de cristina
        """CREATE TABLE hola ( 
            name text,
            money integer
            )"""
    )
    conn.commit()
    conn.close()

def insertRow(name,money): #meter una fila
    conn = sql.connect("hola.db")
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"INSERT INTO hola VALUES ('{name}', {money})"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def readRows (): #leer filas 
    conn = sql.connect("hola.db")
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"SELECT * from  hola"
    cursor.execute(instruccion)
    datos = cursor.fetchall() #nos devuelve todos los datos seleccionados
    conn.commit()
    conn.close()
    print(datos)

def insertRows (list): #meter varias filas
    conn = sql.connect("hola.db")
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"INSERT INTO hola VALUES (?,?)"
    cursor.executemany(instruccion,list) #utilizamos esta funcion porque vamos a insertar varios
    conn.commit()
    conn.close()
def readOrdered (field) : #leer en orden
    conn = sql.connect("hola.db")
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"SELECT * from  hola ORDER BY {field} DESC"
    cursor.execute(instruccion)
    datos = cursor.fetchall() #nos devuelve todos los datos seleccionados
    conn.commit()
    conn.close()
    print(datos)

def search (): #hacer consultas
    conn = sql.connect("hola.db")
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"SELECT * from  hola WHERE name = 'nombre'" #cambiar nombre por cualquier valor de la tabla
    cursor.execute(instruccion)
    datos = cursor.fetchall() #nos devuelve todos los datos seleccionados
    conn.commit()
    conn.close()
    print(datos)

def updateFields(): #modificar
    conn = sql.connect("hola.db")
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"UPDATE hola SET money = 1000 WHERE name like 'julian')"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def deleteRow(): #borrar filas
    conn = sql.connect("hola.db")
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    instruccion = f"DELETE FROM hola WHERE name = 'julian'" #cambiar nombre por cualquier valor de la tabla
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    #createTable() #ejecuto y luego hago ctrl+shift+P para buscar las bases de datos
    #insertRow("juan", 100) #cada vez que vuelvo a hacer una insercción tengo que darle al play en la bbdd (abajo a la izqda)
    #readRows()
    lista = [
        ("julian",1000),
        ("antonio",11)
        ]
    #insertRows(lista) #ejecuto la lista antes 
    #readOrdered()
    #search()
    #updateFields()
    #deleteRow()
        