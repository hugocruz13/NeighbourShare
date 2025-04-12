import hashlib
import os
import base64
import re

from fastapi import HTTPException


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

print(hash_password("123456"))

def validate_password_strength(password: str) -> str:
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d])([^\s]){8,}$'
    if not re.match(pattern, password):
        raise HTTPException(
            status_code=400,
            detail="Senha inválida: deve ter no mínimo 8 caracteres, incluindo uma letra maiúscula, uma minúscula, um número e um caractere especial."
        )
    return password

