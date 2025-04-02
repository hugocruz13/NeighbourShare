import os
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from db.session import get_db
from middleware.auth_middleware import jwt_middleware, verify_token_signup, role_required
from schemas.user_schemas import UserRegistar, UserLogin, UserJWT, NewUserUpdate
from services.auth_service import registar_utilizador, user_valido, verificao_novo_utilizador, atualizar_novo_utilizador
from fastapi.responses import RedirectResponse

# Define o tempo do token
EXPIRE_MINUTES_LOGIN = int(os.getenv("EXPIRE_MINUTES_LOGIN"))

router = APIRouter()

#Controler login, protegido
@router.post("/registar")
async def registar(user: UserRegistar, token: UserJWT = Depends(role_required(["admin"])), db: Session = Depends(get_db)):
    try:
        sucesso, mensagem = await registar_utilizador(user, db)
        if sucesso:
            return {"message": "Registo realizado com sucesso"}
        else:
            raise HTTPException(status_code=400, detail=mensagem)  # Erro
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail= {str(e)})

# Controller login
@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db), response: Response = Response):
    try:
        sucesso, mensagem = await user_valido(db, user)

        if sucesso:
            # Define o cookie de login
            response.set_cookie(
                key="access_token",
                value=mensagem,
                httponly=True,  # Impede acesso via JavaScript
                secure=True,  # Garante que o cookie seja enviado apenas por HTTPS
                samesite="strict",  # Controle de onde o cookie é enviado (Lax ou Strict)
                expires=datetime.now(timezone.utc) + timedelta(minutes=int(EXPIRE_MINUTES_LOGIN)),  # Expiração
            )
            return {"message": "Login com sucesso"}
        else:
            raise HTTPException(status_code=401, detail=mensagem)  # Erro de login
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})

@router.get("/verification/{token}")
async def verificacao(token, db:Session = Depends(get_db)):
    try:
        print(token)
        payload = verify_token_signup(token)
        user = UserJWT(id=payload["id"], email=payload["email"], role=payload["role"])
        if await verificao_novo_utilizador(db, user):
            # Redirecionar para página de atualizar dados para completar registo
            return RedirectResponse(url=f"http://127.0.0.1:8000/docs#/default/registar_atualizar_dados_api_registar_atualizar_dados_post?{token}") #TODO ALTERAR A URL
        else:
            raise HTTPException(status_code=400, detail="Token de verificação de email inválido")
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})

@router.post("/registar/atualizar_dados")
async def registar_atualizar_dados(user: NewUserUpdate, token: str, db: Session = Depends(get_db)):
    try:
        payload = verify_token_signup(token)
        user_jwt = UserJWT(id=payload["id"], email=payload["email"], role=payload["role"])
        return await atualizar_novo_utilizador(user, user_jwt, db)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})
