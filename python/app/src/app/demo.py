from app.usuario import Usuario
from app.setup import inicializar_usuario, obtener_ip, cifrar_ip
from app.contrato import Contrato
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives.asymmetric.padding import MGF1
from cryptography.hazmat.primitives.hashes import SHA256
import binascii

def main():
    print("Creando usuario...")
    user = inicializar_usuario()
    print("\t\t\t[COMPLETADO]")

    print("Obtieniendo IP del usuario...")
    ip = obtener_ip()
    print("\t\t\t[COMPLETADO -> IP: {ip}]".format(ip = ip))

    print("Cifrando dirección IP")
    ip_cifrada = cifrar_ip(user)
    print("\t\t\t[COMPLETADO]")
    print("\n---> IP Cifrada: {ip}\n".format(ip = binascii.hexlify(ip_cifrada).decode('utf-8')))

    print("Creando contrato...")
    contract = Contrato()
    print("\t\t\t[COMPLETADO]")

    print("Actualizando TestNet...")
    contract.actualizar_ip(
        binascii.hexlify(user.hash).decode('utf-8'), 
        binascii.hexlify(ip_cifrada).decode('utf-8')
    )
    print("\t\t\t[COMPLETADO]")

    print("Consultando TestNet...")
    respuesta = contract.consultar_ip(
        binascii.hexlify(user.hash).decode('utf-8')
    )
    print("\t\t\t[COMPLETADO]")
    print("\n---> Respuesta: {}\n".format(respuesta))

    print("Desencriptando resultado...")
    ip_descifrada = user.priv_key.decrypt(
        bytes.fromhex(respuesta),
        OAEP(
            mgf=MGF1(SHA256()),
            algorithm=SHA256(),
            label=None
        )
    )
    print("\t\t\t[COMPLETADO -> IP descifrada: {ip}]".format(ip = ip_descifrada.decode('utf-8')))

main()