from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

class Usuario:
    def __init__(self, hash, pub_key, priv_key):
        self.hash = hash
        self.pub_key = pub_key
        self.priv_key = priv_key