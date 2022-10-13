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
    print("Cargando Chat...")
    chat = leer_chat(open("resources/demo_chat.txt").read().strip())
    
    # Obtenemos la info del contacto y lo añadimos al chat
    hash_contacto = open("resources/hash_contacto.txt").read().strip()
    priv_key_contacto = string_to_priv_key(open("resources/priv_key_contacto.txt").read().strip())
    ip_contacto = hash_to_string(
        priv_key_contacto.decrypt(
            ciphertext=contract.consultar_ip(hash_contacto),
            padding=OAEP(
                mgf=MGF1(SHA256()),
                algorithm=SHA256(),
                label=None
            )
        )
    )
    chat.addMiembro(Contacto(chat.pub_key, ip_contacto, string_to_hash(hash_contacto)))
    print("\t\t\t[COMPLETADO]")

    # Si somos el usuario A y no es la primera ejecución, enviamos un mensaje al usuario B
    if (sys.argv[1] == "user_a"):
        # Creamos un mensaje
        print("Enviando Mensaje...")
        message = Mensaje("texto_prueba", hash_to_string(chat.id_chat))

        # Enviamos el mensaje
        await chat.send_message(message)
        print("\t\t\t[COMPLETADO]")

    else:
        # Si no, esperamos a recibir un mensaje y lo mostramos
        read = False
        mensajes = []
        print("Esperando Mensaje...")
        while not read:
            # Verificamos si hay algún mensaje nuevo
            mensajes = chat.read_new_messages()
            read = len(mensajes) > 0

            # Esperamos 1 segundo
            sleep(1)
        print("\t\t\t[COMPLETADO]")

        # Mostramos el mensaje leído
        for m in mensajes:
            print(m.to_json())

asyncio.run(main())