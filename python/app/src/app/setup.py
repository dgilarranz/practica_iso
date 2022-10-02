from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

def inicializar_usuario():
    priv_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    pub_key = priv_key.public_key()

    # Obtenemos el hash del usuario a partir de su clave pública
    user_hash = hashes.Hash(hashes.SHA256())
    user_hash.update(
        pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )
    
    user = {
        'hash': user_hash.finalize(),
        'pub_key': pub_key,
        'priv_key': priv_key
    }

    return user



    

