from app.usuario import Usuario
from app.setup import inicializar_usuario, obtener_ip, cifrar_ip
from app.contrato import Contrato

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

    print("Creando contrato...")
    contract = Contrato()
    print("\t\t\t[COMPLETADO]")

    print("Actualizando TestNet...")
    contract.actualizar_ip(user.hash.decode('utf-8', 'ignore'), ip_cifrada.decode('utf-8', 'ignore'))
    print("\t\t\t[COMPLETADO]")

    print("Consultando TestNet...")
    respuesta = contract.consultar_ip(user.hash.decode('utf-8', 'ignore'))
    print("\t\t\t[COMPLETADO -> Respuesta: {}]".format(respuesta))

main()