from unittest.mock import patch
from app.contrato import Contrato
from app.excepciones import NoWeb3Connection
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
import pytest

@patch ('app.contrato.Contrato.TEST_NET_URL', 'http://url_incorrecta.com')
def test_conectar_a_testnet_url_incorrect():
    with pytest.raises(NoWeb3Connection):
        Contrato()

def test_conectar_a_testnet_url_correcta():
    address = open('resources/direccion_contrato.txt', 'r').read()
    assert Contrato().contrato.address == address

def test_actualizar_ip():
    assert Contrato().actualizar_ip(
        hash_usuario="hash_usuario_ejemplo",
        ip_cifrada="ip_cifrada_ejemplo"
        ) == True

def test_consultar_ip():
    assert Contrato().consultar_ip("hash_usuario_ejemplo") == "ip_cifrada_ejemplo"
