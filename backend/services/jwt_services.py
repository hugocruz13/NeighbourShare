from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import jwt
import os

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY_LOGIN")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_MINUTES_LOGIN = int(os.getenv("EXPIRE_MINUTES_LOGIN"))

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
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def generate_jwt_token_registo(user_id: int, email: str, role: str) -> str:
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES_LOGIN)
    payload = {
        "id": user_id,
        "email": email,
        "role": role,
        "type": "verification",
        "exp": expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token