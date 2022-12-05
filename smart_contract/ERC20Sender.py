import datetime
import os
import sys
from decimal import Decimal

from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import HTTPProvider, Web3
from web3.middleware import construct_sign_and_send_raw_middleware

from eth_defi.abi import get_deployed_contract
from eth_defi.token import fetch_erc20_details
from eth_defi.txmonitor import wait_transactions_to_complete


# Esta es la dirección en Goerli de nuestro Token ISOCrypto. Para añadir BTC faltaría un switch
ERC_20_TOKEN_ADDRESS = "0x22d5f99dc97608a26Bb051D280BC7316A036a623"

# Connect to JSON-RPC node
json_rpc_url = os.environ["JSON_RPC_URL"]
web3 = Web3(HTTPProvider(json_rpc_url))
print(
    f"Connected to blockchain, chain id is {web3.eth.chain_id}. the latest block is {web3.eth.block_number:,}"
)

# Es necesario contar con la Private Key del usuario (deberá introducirla en un fichero local de Enviromental Variables)
private_key = os.environ.get("PRIVATE_KEY")
assert private_key is not None, "You must set PRIVATE_KEY environment variable"
assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"
account: LocalAccount = Account.from_key(private_key)
web3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))

# Un fetch de la dirección del contrato junto con sus detalles
erc_20 = get_deployed_contract(web3, "ERC20MockDecimals.json", ERC_20_TOKEN_ADDRESS)
token_details = fetch_erc20_details(web3, ERC_20_TOKEN_ADDRESS)

print(f"Token details are {token_details}")

balance = erc_20.functions.balanceOf(account.address).call()
eth_balance = web3.eth.getBalance(account.address)

print(
    f"Your balance is: {token_details.convert_to_decimals(balance)} {token_details.symbol}"
)
print(f"Your have : {eth_balance/(10**18)} ETH for gas fees")

# Introducimos el valor decimal de tokens a transferir y la dirección destino
decimal_amount = input("How many tokens to transfer? ")
to_address = input("Give destination Ethereum address? ")

# Parámetros para validar el input de ISOToken
try:
    decimal_amount = Decimal(decimal_amount)
except ValueError as e:
    raise AssertionError(f"Not a good decimal amount: {decimal_amount}") from e

assert web3.isChecksumAddress(to_address), f"Not a valid address: {to_address}"

# Exigimos al usuario confirmar la transacción
print(f"Confirm transfering {decimal_amount} {token_details.symbol} to {to_address}")
confirm = input("Ok [y/n]?")
if not confirm.lower().startswith("y"):
    print("Aborted")
    sys.exit(1)

# Cambiar el dato decimal del usuario a WETH (*10^18)
raw_amount = token_details.convert_to_raw(decimal_amount)
tx_hash = erc_20.functions.transfer(to_address, raw_amount).transact(
    {"from": account.address}
)

# Lanza una excepción si el usuario no ha confirmado previamente la transacción a realizar
print(f"Broadcasted transaction {tx_hash.hex()}, now waiting 5 minutes for mining")
wait_transactions_to_complete(
    web3, [tx_hash], max_timeout=datetime.timedelta(minutes=5)
)

print("All ok!")
