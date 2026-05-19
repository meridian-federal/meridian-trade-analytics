"""Legacy trade signing. Migration to PQC tracked under TICK-5102."""
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend


def sign_trade(trade_bytes: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
    return private_key.sign(
        trade_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )


def load_private_key(pem_bytes: bytes) -> rsa.RSAPrivateKey:
    return serialization.load_pem_private_key(
        pem_bytes, password=None, backend=default_backend()
    )
