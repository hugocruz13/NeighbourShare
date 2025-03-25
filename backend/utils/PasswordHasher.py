import hashlib
import os
import base64


def hash_password(password: str) -> tuple[str, str]:
    """
    Gera um hash PBKDF2 da password e um salt aleatório.
    """
    salt = os.urandom(16)  # Gera um salt aleatório de 16 bytes
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256', password.encode(), salt, 100000, dklen=32
    )

    # Converte para base64 para armazenamento
    salt_str = base64.b64encode(salt).decode()
    hash_str = base64.b64encode(hashed_password).decode()

    return hash_str, salt_str


def verificar_password(password: str, stored_hash: str, stored_salt: str) -> bool:
    """
    Verifica se a password fornecida corresponde ao hash armazenado.
    """
    salt = base64.b64decode(stored_salt)  # Converte o salt armazenado para bytes
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256', password.encode(), salt, 100000, dklen=32
    )

    # Converte para base64 para comparar
    return base64.b64encode(hashed_password).decode() == stored_hash
