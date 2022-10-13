import asyncio
from ssl import HAS_TLSv1
from time import sleep
from app.contacto import Contacto
from app.mensaje import Mensaje
from app.usuario import Usuario
from app.setup import inicializar_usuario, obtener_ip, cifrar_ip, obtener_ip_privada
from app.contrato import Contrato
from app.cyphersuite import hash_to_string, string_to_hash, pub_key_to_string, string_to_pub_key, priv_key_to_string, string_to_priv_key
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives.asymmetric.padding import MGF1
from cryptography.hazmat.primitives.hashes import SHA256
from app.crud import leer_chat, insertar_mensaje
import binascii
import os
import file_manager
import sys

async def main():
    # Si es la primera ejecución, se crea y guarda un usuario
    print("Cargando configuración...")
    user = file_manager.leer_usuario()
    print("\t\t\t[COMPLETADO]")
    
    print("Obteniendo IP del usuario...")
    ip = obtener_ip_privada()
    print("\t\t\t[COMPLETADO -> IP: {ip}]".format(ip = ip))

    print("Cifrando dirección IP")
    ip_cifrada = cifrar_ip(user, ip)
    print("\t\t\t[COMPLETADO]")

    print("Actualizando TestNet...")
    contract = Contrato()
    contract.actualizar_ip(
        hash_to_string(user.hash), 
        hash_to_string(ip_cifrada)
    )
    print("\t\t\t[COMPLETADO]")

    # Recuperamos el chat de la Base de Datos
    chat = leer_chat(open("resources/demo_chat.txt").read())
    
    # Obtenemos la info del contacto y lo añadimos al chat
    hash_contacto = open("resources/hash_contacto.txt").read()
    ip_contacto = contract.consultar_ip(hash_contacto)
    chat.addMiembro(Contacto(chat.pub_key, ip_contacto, string_to_hash(hash_contacto)))

    # Si somos el usuario A y no es la primera ejecución, enviamos un mensaje al usuario B
    if (sys.argv[1] == "user_a"):
        # Creamos un mensaje
        message = Mensaje("texto_prueba", hash_to_string(chat.id_chat))

        # Enviamos el mensaje
        await chat.send_message(message)

    else:
        # Si no, esperamos a recibir un mensaje y lo mostramos
        read = False
        mensajes = []
        while not read:
            # Verificamos si hay algún mensaje nuevo
            mensajes = chat.read_new_messages()
            read = len(mensajes) > 0

            # Esperamos 1 segundo
            sleep(1)
        
        # Mostramos el mensaje leído
        for m in mensajes:
            print(m.to_json())

asyncio.run(main)