import sqlite3 as sql
import pytest

@pytest.fixture

def crear_datos_para_test():
    conn = sql.connect("resources/pruebas.db") #cambiar nombre de la bbdd con el nombre de cristina
    cursor = conn.cursor() #nos proporciona el objeto de la conexión
    cursor.execute( #otra vez depende de cristina
        """CREATE TABLE usuario ( 
            hash blob,
            pub_key blob,
            priv_key blob,
            PRIMARY KEY(hash)
            )"""
    )
    instruccion = f"INSERT INTO usuario VALUES ({hash}, {pub_key}, {priv_key})".format(hash=b"0xa",pub_key=b"0xb",priv_key=b"0xc")
    cursor.execute(instruccion)
    conn.commit()
    conn.close()
