import os
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.user_schemas import UserRegistar, UserLogin
from services.auth_service import registar_utilizador, user_valido, verificar_token_cookie

# Define o tempo do token
EXPIRE_MINUTES = int(os.getenv("EXPIRE_MINUTES", 30))

router = APIRouter()

@router.post("/registar")
async def registar(user: UserRegistar, db: Session = Depends(get_db)):
    try:
        sucesso, mensagem = await registar_utilizador(user, db)
        if sucesso:
            return {"message": "Registo realizado com sucesso"}
        else:
            raise HTTPException(status_code=401, detail=mensagem)  # Erro
    except Exception as e:
        raise HTTPException(status_code=500, detail= {str(e)})

@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db), response: Response = Response):
    try:
        sucesso, mensagem = await user_valido(db, user)
        if sucesso:
            # Define o cookie de login com o tempo de expiração
            response.set_cookie(
                key="access_token",
                value=mensagem,
                httponly=True,  # Impede acesso via JavaScript
                secure=True,  # Garante que o cookie seja enviado apenas por HTTPS
                samesite="Strict",  # Controle de onde o cookie é enviado (Lax ou Strict)
                expires=datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES),  # Expiração
            )

            return {"message": "Login com sucesso"}
        else:
            raise HTTPException(status_code=401, detail=mensagem)  # Erro de login
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})

@router.get("/dados_protegidos")
async def dados_protegidos(user: dict = Depends(verificar_token_cookie)):
    return {"message": "Acesso autorizado!", "user": user}