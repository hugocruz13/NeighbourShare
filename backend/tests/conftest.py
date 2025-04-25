import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from main import app
from db.session import SessionLocal
from middleware.auth_middleware import generate_jwt_token_login
from db.models import Utilizador
import datetime

#Cria uma sessão com transação isolada
@pytest.fixture(scope="function")
def db_session():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

@pytest.fixture
def client():
    client = TestClient(app)
    return client

@pytest.fixture
def token_admin():
    payload = {
        "sub": "adminuser",
        "role": "admin",
        "email": "admin@example.com",
        "id": 1
    }
    # Gerar um token admin para os testes que necessitam de um token válido
    token = generate_jwt_token_login(payload["id"], payload["email"], payload["role"])

    return token

def token_user(id_user:int, role:str,email:str):
    payload = {
        "role": role,
        "email": email,
        "id": id_user
    }

    token = generate_jwt_token_login(payload["id"], payload["email"], payload["role"])

    return token

@pytest.fixture
def utilizador_registado(db_session):
    utilizador = Utilizador(
        NomeUtilizador="TesteVerificacao",
        DataNasc=datetime.date(2025, 4, 19),
        Contacto=123456789,
        Email="teste@exemploteste.com",
        PasswordHash="fake_hash",
        Salt="fake_salt",
        Verificado=False,
        TUID=2
    )
    db_session.add(utilizador)
    db_session.commit()
    return db_session.query(Utilizador).filter(Utilizador.Email == utilizador.Email).first()

