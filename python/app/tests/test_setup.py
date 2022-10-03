from app.setup import inicializar_usuario
from cryptography.hazmat.primitives.asymmetric import rsa

def test_inicializar_usuario():
    usuario = inicializar_usuario()

    assert type(usuario['hash']) == bytes
    assert usuario['pub_key'].key_size == 2048
    assert usuario['priv_key'].key_size == 2048
