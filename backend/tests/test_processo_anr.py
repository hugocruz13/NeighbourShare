import httpx
import pytest
import time
from datetime import datetime, date, timedelta
import json
import os
from typing import Dict, Any
from fastapi.testclient import TestClient
from main import app
from db.session import get_db
from sqlalchemy.orm import Session

class DataFlow:
    """Classe para armazenar dados de teste entre várias etapas"""
    def __init__(self):
        self.request_id = None
        self.voting_id = None
        self.budget_voting_id = None
        self.budget_ids = []

@pytest.fixture(scope="module")
def data_flow():
    """Dados compartilhados entre testes"""
    return DataFlow()

@pytest.fixture
def db_session():
    """Cria uma sessão de banco de dados para teste"""
    db = next(get_db())
    yield db
    db.close()

@pytest.fixture
def client():
    """Cria um cliente de teste"""
    with TestClient(app) as client:
        yield client

@pytest.fixture
def residente_data():
    """Credenciais de residente de teste"""
    return {"email": "residente@email.com", "password": "residente"}

@pytest.fixture
def gestor_data():
    """Credenciais de gestor de teste"""
    return {"email": "gestor@email.com", "password": "gestor"}

@pytest.fixture
def residente_token(client, resident_data):
    """Obtém um token de autenticação de residente"""
    response = client.post("/api/login", json=resident_data)
    assert response.status_code == 200, f"Login de residente falhou: {response.text}"
    return response.cookies.get("access_token")

@pytest.fixture
def gestor_token(client, manager_data):
    """Obtém um token de autenticação de gestor"""
    response = client.post("/api/login", json=manager_data)
    assert response.status_code == 200, f"Login de gestor falhou: {response.text}"
    return response.cookies.get("access_token")

@pytest.fixture
def test_pdf_path():
    """Cria um ficheiro PDF de teste para uploads"""
    pdf_path = "tests/test_budget.pdf"
    with open(pdf_path, "w") as f:
        f.write("Conteúdo PDF de teste")
    yield pdf_path
    # Limpeza
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

class TestNewResourceProcess:
    """Teste de integração para o fluxo do processo de aquisição de novo recurso"""
    
    def test_01_create_resource_request(self, client, resident_token, data_flow):
        """Teste de criação de um novo pedido de recurso por um residente"""

        # Armazena ID do pedido para testes subsequentes
        
    
    def test_02_manager_registers_voting(self, client, manager_token, data_flow):
        """Teste de registro de votação pelo gestor para o pedido"""
       
        # Armazena ID da votação para testes subsequentes
    

    def test_03_simulate_votes(self, client, manager_token, data_flow):
        """Teste de simulação de votos de múltiplos residentes"""
        
        # Para fins de teste, lançamos votos manualmente para simular múltiplos usuários
        
    
    def test_04_process_voting_results(self, client, manager_token, data_flow):
        """Teste de processamento dos resultados da votação"""
        
       
    
    def test_05_manager_registers_budgets(self, client, manager_token, data_flow, test_pdf_path):
        """Teste de registro de opções de orçamento pelo gestor"""
        
        # Primeira opção de orçamento
        
        # Segunda opção de orçamento
    

    def test_06_manager_creates_budget_voting(self, client, manager_token, data_flow):
        """Teste de criação de votação para opções de orçamento pelo gestor"""
        
        # Armazena ID da votação de orçamento para testes subsequentes


    def test_07_simulate_budget_votes(self, client, manager_token, data_flow):
        """Teste de simulação de votos para opções de orçamento"""
        
    
    def test_08_process_budget_voting_results(self, client, manager_token, data_flow):
        """Teste de processamento dos resultados da votação de orçamento"""
        

    def test_09_verify_resource_request_state(self, client, manager_token, data_flow):
        """Teste de verificação do estado final do pedido de recurso"""
        
        # Encontra nosso pedido na lista
        
                # Verifica se o estado foi atualizado para refletir a aprovação da compra