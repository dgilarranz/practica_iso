from web3 import Web3
#from dotenv import load_dotenv
import os
import sys

#load_dotenv()

class MoneyContract:
    def __init__(self, from_address: str, private_key: str, token_address: str, eth_amount: str, to_address: str):
        # Es un RPC público de la Testnet de Goerli
        infura_url = "https://goerli.infura.io/v3/054abd12a18c4753845e87dc8e460740"
        web3 = Web3(Web3.HTTPProvider(infura_url))
        transfer_abi = open("resources/transferAbi.json", "r").read()

        nonce = web3.eth.getTransactionCount(from_address)
        contract = web3.eth.contract(address=token_address, abi=transfer_abi)

        # Introducimos el valor decimal de tokens a transferir y la dirección destino
        if not eth_amount.isnumeric():
            raise MoneyTransferError("No es un número, idiota")
        wei_amount = web3.toWei(eth_amount, "ether")

        if not web3.isAddress(to_address):
            raise MoneyTransferError("La address siguiente no es correcta: {toAddress}")

        if not to_address != from_address:
            raise MoneyTransferError("No te puedes enviar a tí mismo bobo")

        contractCall = contract.functions.transfer(to_address, wei_amount)
        unsignedTransaction = contractCall.buildTransaction(
            {"chainId": 5, "from": from_address, "nonce": nonce}
        )

        signed_txn = web3.eth.account.sign_transaction(
            unsignedTransaction, private_key=private_key
        )
        web3.eth.sendRawTransaction(signed_txn.rawTransaction)

        print("Todo bien cryptobro!")

class MoneyTransferError(Exception):
    def __init__(self, msg: str):
        self.msg = msg


# Disclaimer for DEVS
# Dirección origen de prueba = "0xf463c820487b22C2fe4d9dCbfAf0Df7aC8C7C16f"
# Clave Privada de Dicha dirección = "1b8fedebfee46a099a7fe9d83259f3670bf79da3e4953fbb6a2c114ec0dd1349"
# Dirección destino de prueba = "0xa70A8cfcBdCA900bf0431FE376A7243C4424Fa2f"
# Dirección token ISOCrypto = "0x22d5f99dc97608a26Bb051D280BC7316A036a623"
