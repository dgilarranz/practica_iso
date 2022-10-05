import web3
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3.middleware import construct_sign_and_send_raw_middleware
from app.excepciones import NoWeb3Connection

class Contrato:
    """Clase que encapsula las interacciones con el SmartContract desplegado"""

    TEST_NET_URL = 'https://goerli.infura.io/v3/054abd12a18c4753845e87dc8e460740'
    
    def __init__(self):
        self.owner = open('resources/owner_address.txt', 'r').read()
        self.w3 = self.__conectar_a_testnet()
        self.contrato = self.__conectar_a_contrato()

    def __conectar_a_testnet(self):
        # Nos conectamos a la TestNet
        w3 = web3.Web3(web3.HTTPProvider(self.TEST_NET_URL))

        if not w3.isConnected():
            raise NoWeb3Connection

        # Creamos la cuenta que se usará para las transacciones
        cuenta = Account.from_key(open('resources/account_key.txt', 'r').read())
        w3.middleware_onion.add(construct_sign_and_send_raw_middleware(cuenta))
        w3.eth.default_account = cuenta

        return w3


    def __conectar_a_contrato(self):
        # Obtenemos el contrato (necesitamos abi y dirección)
        address = open('resources/direccion_contrato.txt', 'r').read()
        abi = open('resources/abi.json', 'r').read()
    
        return self.w3.eth.contract(address=address, abi=abi)
    
    def actualizar_ip(self, hash_usuario, ip_cifrada):
        try:
            txn_hash = self.contrato.functions.updateIp(hash_usuario, ip_cifrada).transact(
                {
                    'from': self.owner
                }
            )
            self.w3.eth.waitForTransactionReceipt(txn_hash)
        except Exception as e:
            print(e.args)
            return False
        else:
            return True

    def consultar_ip(self, hash_usuario):
        return self.contrato.functions.getIp(hash_usuario).call({'from': self.owner})
        


