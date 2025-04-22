from fastapi import HTTPException, Request, Response, Depends
from fastapi.security import HTTPBearer
from schemas.user_schemas import UserJWT
from services.jwt_services import generate_jwt_token_login
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from typing import List
import jwt
import os

# Load environment variables
load_dotenv()

# Recolhe os dados armazenados no ficheiro .env
SECRET_KEY_LOGIN = os.getenv("SECRET_KEY_LOGIN")
SECRET_KEY_SIGNUP = os.getenv("SECRET_KEY_SIGNUP")
SECRET_KEY_RECOVERY = os.getenv("SECRET_KEY_RECOVERY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_MINUTES_LOGIN = int(os.getenv("EXPIRE_MINUTES_LOGIN"))
EXPIRE_MINUTES_SIGNUP = int(os.getenv("EXPIRE_MINUTES_SIGNUP"))

sucurity = HTTPBearer()

# Função que realiza a verificação do token login
def verify_token_login(token: str):
    try:
        # Descodifica o token
        payload = jwt.decode(token, SECRET_KEY_LOGIN, algorithms=[ALGORITHM])
        type = payload.get("type")

        if type != "access":
            raise HTTPException(status_code=401,detail="Token inválido")

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

# Função que realiza a verificação do token de verificação email
def verify_token_verification(token: str):
    try:
        # Descodifica o token
        payload = jwt.decode(token, SECRET_KEY_SIGNUP, algorithms=[ALGORITHM])
        type = payload.get("type")

        if type != "verification":
            raise HTTPException(status_code=401,detail="Token inválido")

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

# Função que realiza a verificação do token de recuperação password
def verify_token_recuperacao(token: str):
    try:
        # Descodifica o token
        payload = jwt.decode(token, SECRET_KEY_RECOVERY, algorithms=[ALGORITHM])
        type = payload.get("type")

        if type != "recovery":
            raise HTTPException(status_code=401,detail="Token inválido")

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

# Função responsável por obter o token
async def jwt_middleware(request: Request, response: Response):

    # Obter token armazenado no cookie "access_token"
    token = request.cookies.get("access_token")

    # Verifica se o cliente contém o token
    if not token:
        raise HTTPException(status_code=403, detail="Token ausente")

    # Verifica se o token é valido
    if not verify_token_login(token):
        raise HTTPException(status_code=403, detail="Token invalido")

    # Descodifica e extrai o tempo
    payload = verify_token_login(token)
    exp = payload.get("exp")

    # Converte o token num objeto
    user_id = payload["id"]
    email = payload["email"]
    role = payload["role"]
    user=UserJWT(id=user_id, email=email, role=role)

    if exp - datetime.now(timezone.utc).timestamp() < 5 * 60:

        new_token = generate_jwt_token_login(user_id, email, role)

        response.set_cookie(
            key="access_token",
            value=new_token,
            httponly=True,  # Impede acesso via JavaScript
            secure=True,  # Garante que o cookie seja enviado apenas por HTTPS
            samesite="strict",  # Controle de onde o cookie é enviado (Lax ou Strict)
            expires=datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES_LOGIN),  # Expiração
        )

    return user

def role_required(roles: List[str]):
    def role_check(user: UserJWT = Depends(jwt_middleware)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Acesso negado")
        return user
    return role_check