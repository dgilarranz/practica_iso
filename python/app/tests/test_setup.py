from unittest.mock import MagicMock, patch
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives.asymmetric.padding import MGF1
from cryptography.hazmat.primitives.hashes import SHA256
from app.setup import inicializar_usuario
from app.setup import obtener_ip
from app.setup import cifrar_ip

def test_inicializar_usuario():
    usuario = inicializar_usuario()

    assert type(usuario.hash) == bytes
    assert usuario.pub_key.key_size == 2048
    assert usuario.priv_key.key_size == 2048

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

@patch ('app.setup.obtener_ip')
def test_cifrar_ip(mock_obtener_ip):
    # Mockeamos la respuesta de la función obtener_ip()
    ip_prueba = '128.53.23.94'
    mock_obtener_ip.return_value = ip_prueba

    # Obtenemos la ip cifrada
    user = inicializar_usuario()
    ip_cifrada = cifrar_ip(user)

    # Verificamos que al desencriptar la ip, obtenemos la misma
    assert user.priv_key.decrypt(ip_cifrada, OAEP(mgf=MGF1(SHA256()), algorithm=SHA256(), label=None))

    
