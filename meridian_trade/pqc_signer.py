"""PQC trade signing path. Rolled out to 40% of trades as of 2026-04-15."""
from pqcrypto.sign import ml_dsa_65 as mldsa65
from pqc_types import MLDSAPrivateKey, MLDSAPublicKey


def sign_trade_pqc(trade_bytes: bytes, private_key: MLDSAPrivateKey) -> bytes:
    return mldsa65.sign(private_key.raw, trade_bytes)


def verify_trade_pqc(trade_bytes: bytes, signature: bytes, public_key: MLDSAPublicKey) -> bool:
    try:
        mldsa65.verify(public_key.raw, trade_bytes, signature)
        return True
    except Exception:
        return False


def generate_pqc_keypair() -> tuple[MLDSAPrivateKey, MLDSAPublicKey]:
    pk_bytes, sk_bytes = mldsa65.keypair()
    return MLDSAPrivateKey(raw=sk_bytes), MLDSAPublicKey(raw=pk_bytes)
