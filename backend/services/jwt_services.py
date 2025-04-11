from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import jwt
import os

# Load environment variables
load_dotenv()

SECRET_KEY_LOGIN = os.getenv("SECRET_KEY_LOGIN")
SECRET_KEY_SIGNUP = os.getenv("SECRET_KEY_SIGNUP")
SECRET_KEY_RECOVERY = os.getenv("SECRET_KEY_RECOVERY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_MINUTES_LOGIN = int(os.getenv("EXPIRE_MINUTES_LOGIN"))
EXPIRE_MINUTES_REGISTO = int(os.getenv("EXPIRE_MINUTES_SIGNUP"))

def generate_jwt_token_login(user_id: int, email: str, role: str) -> str:

    # Define o tempo do token
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES_LOGIN)

    # Claims token JWT (informação util)
    payload = {
        "id": user_id,
        "email": email,
        "role": role,
        "type": "access",
        "exp": expiration_time
    }

    # Cria o token
    token = jwt.encode(payload, SECRET_KEY_LOGIN, algorithm=ALGORITHM)
    return token

def generate_jwt_token_registo(email: str, role: str, id_utilizador: int) -> str:
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES_REGISTO)
    payload = {
        "id": id_utilizador,
        "email": email,
        "role": role,
        "type": "verification",
        "exp": expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY_SIGNUP, algorithm=ALGORITHM)
    return token, expiration_time

def generate_jwt_token_recovery(user_id: int, email: str) -> str:
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES_LOGIN)
    payload = {
        "id": user_id,
        "email": email,
        "type": "recovery",
        "exp": expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY_RECOVERY, algorithm=ALGORITHM)
    return token, expiration_time