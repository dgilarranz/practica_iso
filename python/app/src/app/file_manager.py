from app.cyphersuite import hash_to_string, string_to_hash
from app.usuario import Usuario
import json
from cryptography.hazmat.primitives import serialization 
import binascii

FICHERO_CONFIG = "resources/config.json"

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
    user_json['key'] = hash_to_string(usuario.key)

    fichero = open(FICHERO_CONFIG,'w') 
    user_string = json.dumps(user_json)
    #print(user_json)
    fichero.write(user_string) 
    fichero.close() 

def leer_usuario() -> Usuario:
    # Abrimos el fichero en modo lectura
    f = open(FICHERO_CONFIG, "r")

    # Leemos el fichero y lo guardamos en una estructura json
    json_contents = json.load(f)

    # Obtenemos los atributos del usuario
    user_hash = binascii.unhexlify(json_contents['hash'].encode('utf-8'))
    pub_key = serialization.load_pem_public_key(
        binascii.unhexlify(json_contents['pub_key'].encode('utf-8'))
    )
    priv_key = serialization.load_pem_private_key(
        binascii.unhexlify(json_contents['priv_key'].encode('utf-8')),
        None
    )

    key = string_to_hash(json_contents['key'])

    # Devolvemos un objeto usuario con los atributos leídos
    return Usuario(user_hash, pub_key, priv_key, key)
    
    
