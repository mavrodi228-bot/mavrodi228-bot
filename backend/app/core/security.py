import base64
from cryptography.fernet import Fernet
from app.core.config import get_settings


def get_fernet() -> Fernet:
    key = get_settings().encryption_key.encode()
    if len(key) != 44:
        key = base64.urlsafe_b64encode(key.ljust(32, b'0')[:32])
    return Fernet(key)


def encrypt_text(value: str) -> str:
    return get_fernet().encrypt(value.encode()).decode()


def decrypt_text(value: str) -> str:
    return get_fernet().decrypt(value.encode()).decode()
