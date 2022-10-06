from app.usuario import Usuario
import json
from cryptography.hazmat.primitives import serialization 
import binascii

def guardar_usuario(usuario: Usuario) -> None:
    user_json = {}
    user_json['hash'] = binascii.hexlify(usuario.hash).decode('UTF-8')
    pub_key_string = binascii.hexlify(
            usuario.pub_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        ).decode('UTF-8')
    user_json['pub_key'] = pub_key_string
    priv_key_string = binascii.hexlify(
            usuario.priv_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        ).decode('UTF-8')
    #print(priv_key_string)
    #print(type(priv_key_string))

    user_json['priv_key'] = priv_key_string

    fichero = open('resources/config.json','w') 
    user_string = json.dumps(user_json)
    #print(user_json)
    fichero.write(user_string) 
    fichero.close() 

    
