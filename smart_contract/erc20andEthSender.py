from web3 import Web3
from dotenv import load_dotenv
import os
import sys

load_dotenv()

# Es un RPC público de la Testnet de Goerli
infura_url = "https://goerli.infura.io/v3/054abd12a18c4753845e87dc8e460740"
web3 = Web3(Web3.HTTPProvider(infura_url))
transferAbi = open("transferAbi.json", "r").read()

# El cliente introduce sus datos relatvos a su cartera
fromAddress = input("Introduce tu dirección DESDE donde quieres enviar los tokens\n")
PRIVATE_KEY = input(
    "Introduce la PRIVATE KEY asociada a tu cartera. \nDisclaimer: Este dato NO SE GUARDA EN LA APP, es local para tí.\n"
)


nonce = web3.eth.getTransactionCount(fromAddress)

# El cliente introduce la dirección del contrato asociada al token.
tokenAddress = input("Introduce la dirección del token que quieres transferir\n")

contract = web3.eth.contract(address=tokenAddress, abi=transferAbi)

# Introducimos el valor decimal de tokens a transferir y la dirección destino
ethAmount = input("Cuantos ISOCryptos quieres enviar?\n")
assert ethAmount.isnumeric(), f"No es un número, idiota"
weiAmount = web3.toWei(ethAmount, "ether")
toAddress = input(
    "Escribe la dirección de destino a la que quieras enviar el dinerete\n"
)
assert web3.isAddress(toAddress), f"La address siguiente no es correcta: {toAddress}\n"
assert toAddress != fromAddress, f"No te puedes enviar a tí mismo bobo\n"

# Confirmación de la transaction
confirm = input("Ok [y/n]?")
if not confirm.lower().startswith("y"):
    print("Aborted")
    sys.exit(1)


contractCall = contract.functions.transfer(toAddress, weiAmount)
unsignedTransaction = contractCall.buildTransaction(
    {"chainId": 5, "from": fromAddress, "nonce": nonce}
)

signed_txn = web3.eth.account.sign_transaction(
    unsignedTransaction, private_key=PRIVATE_KEY
)
web3.eth.sendRawTransaction(signed_txn.rawTransaction)

print("Todo bien cryptobro!")


# Disclaimer for DEVS
# Dirección origen de prueba = "0xf463c820487b22C2fe4d9dCbfAf0Df7aC8C7C16f"
# Clave Privada de Dicha dirección = "1b8fedebfee46a099a7fe9d83259f3670bf79da3e4953fbb6a2c114ec0dd1349"
# Dirección destino de prueba = "0xa70A8cfcBdCA900bf0431FE376A7243C4424Fa2f"
# Dirección token ISOCrypto = "0x22d5f99dc97608a26Bb051D280BC7316A036a623"
