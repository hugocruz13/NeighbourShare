import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from main import app
from db.session import SessionLocal
from middleware.auth_middleware import generate_jwt_token_login

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

