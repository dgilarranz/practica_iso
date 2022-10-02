import web3
from app.excepciones import NoWeb3Connection

class Contrato:
    """Clase que encapsula las interacciones con el SmartContract desplegado"""

    TEST_NET_URL = 'https://goerli.infura.io/v3/054abd12a18c4753845e87dc8e460740'
    
    def __init__(self):
        self.owner = open('resources/owner_address.txt', 'r').read()
        self.contrato = self.__conectar_a_contrato()

    def __conectar_a_contrato(self):
        # Nos conectamos a la TestNet
        w3 = web3.Web3(web3.HTTPProvider(self.TEST_NET_URL))

        if not w3.isConnected():
            raise NoWeb3Connection

        # Obtenemos el contrato (necesitamos abi y dirección)
        address = open('resources/direccion_contrato.txt', 'r').read()
        abi = open('resources/abi.json', 'r').read()

        return w3.eth.contract(address=address, abi=abi)
    
    def actualizar_ip(self, hash_usuario, ip_cifrada):
        try:
            self.contrato.functions.updateIp(hash_usuario, ip_cifrada).transact()
        except Exception:
            return False
        else:
            return True

    def consultar_ip(self, hash_usuario):
        return self.contrato.functions.getIp(hash_usuario).call()
        


