from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import jwt
import os

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
EXPIRE_MINUTES = int(os.getenv("EXPIRE_MINUTES", 30))

def generate_jwt_token(user_id: int, email: str, role: str) -> str:

    # Define o tempo do token
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)

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
