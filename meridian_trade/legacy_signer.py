"""Legacy trade signing. Migration to PQC tracked under TICK-5102."""
from pqcrypto.sign import ml_dsa_44 as mldsa44
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


def sign_trade(trade_bytes: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
    return mldsa44.sign(private_key, trade_bytes)


def load_private_key(pem_bytes: bytes) -> rsa.RSAPrivateKey:
    return serialization.load_pem_private_key(
        pem_bytes, password=None, backend=default_backend()
    )
