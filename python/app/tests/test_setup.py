from unittest.mock import MagicMock, patch
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives.asymmetric.padding import MGF1
from cryptography.hazmat.primitives.hashes import SHA256
from app.cyphersuite import descifrar_ip
from app.setup import inicializar_usuario
from app.setup import obtener_ip
from app.setup import cifrar_ip
from app.setup import obtener_ip_privada

def test_inicializar_usuario():
    usuario = inicializar_usuario()

    assert type(usuario.hash) == bytes
    assert usuario.pub_key.key_size == 2048
    assert usuario.priv_key.key_size == 2048
    assert type(usuario.key) == bytes

@patch ('app.setup.requests.get')
def test_obtener_ip(mock_requests):
    ip_prueba = '128.53.23.94'

    # Mockeamos la respuesta
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = ip_prueba

    # Especificamos el valor que devuelve el get()
    mock_requests.return_value = mock_response

    assert obtener_ip() == ip_prueba

def test_cifrar_ip():
    ip_prueba = '128.53.23.94'

    # Obtenemos la ip cifrada
    user = inicializar_usuario()
    ip_cifrada = cifrar_ip(user, ip_prueba)

    # Verificamos que al desencriptar la ip, obtenemos la misma
    user.k_pub = user.priv_key
    assert descifrar_ip(user, ip_cifrada) == ip_prueba

@patch('socket.socket.getsockname')
def test_obtener_ip_privada(mock_getsockname):
    # Mockeamos la respuesta de la función getsockname para que sea la ip de prueba
    ip_prueba = '1.1.1.1'
    mock_getsockname.return_value = ['1.1.1.1']

    # Verificamos que se obtiene la IP privada
    assert obtener_ip_privada() == ip_prueba

