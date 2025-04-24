from middleware.auth_middleware import verify_token_login
from main import app
from fastapi.testclient import TestClient
from db.models import Utilizador
import pytest

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def admin_data(db_session):
    user_data = {
        "email": "admin@email.com",
        "password": "admin"
    }
    assert db_session.query(Utilizador).filter(Utilizador.Email == user_data["email"]).first() is not None
    return user_data

def test_login_admin(client, admin_data):
    response = client.post("/api/login", json=admin_data)
    assert response.status_code == 200
    print("Login response:", response.json())

    # Extrai o cookie manualmente (porque o TestClient não o está a guardar automaticamente)
    access_token = response.cookies.get("access_token")
    assert access_token is not None, "Cookie access_token não recebido"
    assert verify_token_login(access_token)

    client.cookies.set("access_token", access_token)

    response = client.get("/api/me")
    print("Status:", response.status_code)
    print("Data:", response.json())
    assert response.status_code == 200
    assert response.json()["role"] == "admin"

