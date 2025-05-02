import pytest
from fastapi.testclient import TestClient
from main import app
from db.models import EntidadeExterna, PedidoManutencao, Manutencao, RecursoComun, Utilizador, Orcamento
from db.session import get_db

import os
os.environ["TESTING"] = "1"

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def db_session():
    db = next(get_db())
    yield db

@pytest.fixture
def entidade_data():
    return {
        "Especialidade": "Tecnologia",
        "Nome": "Entidade Teste",
        "Email": "entidade@teste.com",
        "Contacto": 123456789,
        "Nif": "123456789"
    }

@pytest.fixture
def cookie(client):
    # Perform login as gestor
    login_data = {
        "email": "gestor@email.com",
        "password": "gestor"
    }
    response = client.post("/api/login", json=login_data)
    assert response.status_code == 200

    # Extract token from cookies
    token = response.cookies.get("access_token")
    assert token is not None

    # Return the cookie for use in tests
    return response.cookies

def test_create_entidade(client, db_session, entidade_data, cookie):
    client.cookies.update(cookie)
    client.cookies.set("access_token", cookie.get("access_token"))
    response = client.post("api/entidades/registar", json=entidade_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Entidade registada com sucesso"

    # Verify in database
    db_entidade = db_session.query(EntidadeExterna).filter(EntidadeExterna.Email == entidade_data["Email"]).first()
    assert db_entidade is not None
    assert db_entidade.Nome == entidade_data["Nome"]

def test_view_entidades(client, cookie):
    client.cookies.update(cookie)
    client.cookies.set("access_token", cookie.get("access_token"))
    response = client.get("/api/entidades/ver")
    assert response.status_code == 200
    entidades = response.json()
    assert isinstance(entidades, list)

def test_update_entidade(client, db_session, entidade_data, cookie):
    client.cookies.update(cookie)
    client.cookies.set("access_token", cookie.get("access_token"))
    # Create entidade first
    client.post("/api/entidades/registar", json=entidade_data)
    db_entidade = db_session.query(EntidadeExterna).filter(EntidadeExterna.Email == entidade_data["Email"]).first()
    update_data = {
        "EntidadeID": db_entidade.EntidadeID,
        "Especialidade": "Saúde",
        "Nome": "Entidade Atualizada",
        "Email": "entidade@atualizada.com",
        "Contacto": 987654321,
        "Nif": "987654321"
    }

    response = client.put("api/entidades/update/", json=update_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data[0] is True
    assert "Entidade atualizada com sucesso." in response_data[1]

    # Verify in database
    db_entidade = db_session.query(EntidadeExterna).filter(EntidadeExterna.EntidadeID == update_data["EntidadeID"]).first()
    db_session.refresh(db_entidade)
    assert db_entidade is not None
    assert db_entidade.Nome == update_data["Nome"]

def test_delete_entidade(client, db_session, entidade_data, cookie):
    client.cookies.update(cookie)
    client.cookies.set("access_token", cookie.get("access_token"))
    # Create entidade first
    client.post("api/entidades/registar", json=entidade_data)
    db_entidade = db_session.query(EntidadeExterna).filter(EntidadeExterna.Email == entidade_data["Email"]).first()
    assert db_entidade is not None

    response = client.delete(
        "/api/entidades/eliminar",
        params={"id_entidade": db_entidade.EntidadeID})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data[0] is True
    assert "Entidade removida com sucesso" in response_data[1][0]

    # Verify in database
    db_entidade = db_session.query(EntidadeExterna).filter(EntidadeExterna.EntidadeID == db_entidade.EntidadeID).first()
    assert db_entidade is None