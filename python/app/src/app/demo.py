from time import sleep
from app.usuario import Usuario
from app.setup import inicializar_usuario, obtener_ip, cifrar_ip, obtener_ip_privada
from app.contrato import Contrato
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives.asymmetric.padding import MGF1
from cryptography.hazmat.primitives.hashes import SHA256
import binascii
import os
import file_manager
import sys

def main():
    # Si es la primera ejecución, se crea y guarda un usuario
    user = None
    if not os.path.exists(file_manager.FICHERO_CONFIG):
        print("PRIMERA EJECUCIÓN")
        print("Creando usuario...")
        user = inicializar_usuario()
        print("\t\t\t[COMPLETADO]")
        print("Guardando usuario...")
        file_manager.guardar_usuario(user)
        print("\t\t\t[COMPLETADO]")
    else:
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
        binascii.hexlify(user.hash).decode('utf-8'), 
        binascii.hexlify(ip_cifrada).decode('utf-8')
    )
    print("\t\t\t[COMPLETADO]")

    # Si somos el usuario A, enviamos un mensaje al usuario B
    if (sys.argv[1] == "user_a"):
        # Recuperamos el chat de la Base de Datos
        # COMPLETAR

        # Creamos un mensaje
        # COMPLETAR

        # Enviamos el mensaje
        # Completar -> Chat.enviar_mensaje()
        pass
    else:
        # Si no, esperamos a recibir un mensaje y lo mostramos
        read = False
        while not read:
            # Verificamos si hay algún mensaje nuevo
            # COMPLETAR

            # Esperamos 1 segundo
            sleep(1)
        
        # Mostramos el mensaje leído
        # COMPLETAR

main()