import pytest
import datetime
from fastapi.testclient import TestClient
from main import app
from db.models import PedidoReserva, Reserva, Recurso, EstadoPedidoReserva
from db.session import get_db
import decimal

import os
os.environ["TESTING"] = "1"

"""

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
ANTES DE EXECUTAR O TESTE, VERIFIQUE SE OS IDs DEFINIDOS NO CÓDIGO COMO
A DO UTILIZADOR, ESTÃO A PAR DO QUE ESTÁ NA BASE DE DADOS.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

"""

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def db_session():
    db = next(get_db())
    yield db

@pytest.fixture
def resource_data(db_session):
    novo_recurso = Recurso(
        Nome="Guarda-Sol",
        DescRecurso="Guarda-Sol médido, pode ser usado na praia ou outras áreas de lazer",
        Caucao=decimal.Decimal(20.0),
        UtilizadorID=2,
        DispID=1,
        CatID=1,
        Path="none"
    )
    db_session.add(novo_recurso)
    db_session.commit()
    db_session.refresh(novo_recurso)

    return novo_recurso.RecursoID

@pytest.fixture
def resource_data_indsp(db_session):
    novo_recurso = Recurso(
        Nome="Guarda-Sol",
        DescRecurso="Guarda-Sol médido, pode ser usado na praia ou outras áreas de lazer",
        Caucao=decimal.Decimal(20.0),
        UtilizadorID=2,
        DispID=2,
        CatID=1,
        Path="none"
    )
    db_session.add(novo_recurso)
    db_session.commit()
    db_session.refresh(novo_recurso)

    return novo_recurso.RecursoID

@pytest.fixture
def cookie_residente(client):
    login_data = {
        "email": "residente@email.com",
        "password": "residente"
    }
    response = client.post("/api/login", json=login_data)
    assert response.status_code == 200
    token = response.cookies.get("access_token")
    assert token is not None

    return response.cookies

@pytest.fixture
def cookie_gestor(client):
    login_data = {
        "email": "gestor@email.com",
        "password": "gestor"
    }
    response = client.post("/api/login", json=login_data)
    assert response.status_code == 200
    token = response.cookies.get("access_token")
    assert token is not None
    return response.cookies

@pytest.fixture
def cookie_admin(client):
    login_data = {
        "email": "admin@email.com",
        "password": "admin"
    }
    response = client.post("/api/login", json=login_data)
    assert response.status_code == 200

    token = response.cookies.get("access_token")
    assert token is not None

    return response.cookies


@pytest.fixture
def pedido_reserva_data():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    day_after_tomorrow = tomorrow + datetime.timedelta(days=1)
    
    return {
        "recurso_id": None,
        "data_inicio": tomorrow.isoformat(),
        "data_fim": day_after_tomorrow.isoformat()
    }


class TestFlow:
    def __init__(self):
        self.pedido_reserva_id = None
        self.reserva_id = None


@pytest.fixture(scope="module")
def test_flow():
    return TestFlow()


def test_01_criar_pedido_reserva(client, db_session, cookie_residente, pedido_reserva_data, test_flow, resource_data):
    """Um utilizador pode criar um pedido de reserva de um recurso"""
    client.cookies.set("access_token", cookie_residente.get("access_token"))

    pedido_reserva_data["recurso_id"] = resource_data

    response = client.post(
        "/api/reserva/pedidosreserva/criar",
        data=pedido_reserva_data
    )

    assert response.status_code == 200
    response_data = response.json()
    assert 'Pedido de reserva criado com sucesso!' in str(response_data)

    pedido_reserva = db_session.query(PedidoReserva).order_by(PedidoReserva.PedidoResevaID.desc()).first()
    assert pedido_reserva is not None
    assert pedido_reserva.RecursoID == pedido_reserva_data["recurso_id"]
    assert pedido_reserva.EstadoID == 1  # Estado "Em análise"

    test_flow.pedido_reserva_id = pedido_reserva.PedidoResevaID


def test_02_listar_pedidos_reserva(client, cookie_residente):
    """Um utilizador pode listar seus pedidos de reserva"""
    client.cookies.set("access_token", cookie_residente.get("access_token"))

    response = client.get("/api/reserva/pedidosreserva/lista")
    assert response.status_code == 200
    response_data = response.json()
    
    # Verifica se a resposta contém duas listas (como dono e como solicitante)
    assert len(response_data) == 2
    assert isinstance(response_data[0], list)
    assert isinstance(response_data[1], list)


def test_03_criar_reserva(client, db_session, cookie_gestor, test_flow):
    """O dono do recurso pode aprovar um pedido e criar uma reserva"""
    client.cookies.set("access_token", cookie_gestor.get("access_token"))

    response = client.post(
        f"/api/reserva/criar?pedido_reserva_id={test_flow.pedido_reserva_id}"
    )

    assert response.status_code == 200
    response_data = response.json()
    assert 'Reserva criada com sucesso!' in str(response_data)

    # Verifica se o estado do pedido de reserva foi alterado para "Aprovado"
    pedido_reserva = db_session.query(PedidoReserva).filter(
        PedidoReserva.PedidoResevaID == test_flow.pedido_reserva_id
    ).first()
    assert pedido_reserva is not None
    
    estado = db_session.query(EstadoPedidoReserva).filter(
        EstadoPedidoReserva.EstadoID == pedido_reserva.EstadoID
    ).first()
    assert estado is not None
    assert estado.DescEstadoPedidoReserva == "Aprovado"

    # Verifica se a reserva foi criada
    reserva = db_session.query(Reserva).filter(
        Reserva.PedidoResevaID == test_flow.pedido_reserva_id
    ).first()
    assert reserva is not None
    
    test_flow.reserva_id = reserva.ReservaID


def test_04_listar_reservas(client, cookie_residente):
    """Um utilizador pode listar as reservas"""
    client.cookies.set("access_token", cookie_residente.get("access_token"))

    response = client.get("/api/reserva/lista")
    assert response.status_code == 200
    response_data = response.json()
    
    # Verifica se a resposta contém duas listas (como dono e como solicitante)
    assert len(response_data) == 2
    assert isinstance(response_data[0], list)
    assert isinstance(response_data[1], list)


def test_05_confirmar_entrega_recurso(client, db_session, cookie_gestor, test_flow):
    """Um dono do recurso pode confirmar a entrega do recurso"""
    client.cookies.set("access_token", cookie_gestor.get("access_token"))

    response = client.post(
        f"/api/reserva/confirma/entrega/recurso?reserva_id={test_flow.reserva_id}"
    )

    assert response.status_code == 200
    response_data = response.json()
    assert 'Entrega do produto registada com sucesso!' in str(response_data)

    # Verifica se a flag de entrega foi atualizada no banco de dados
    reserva = db_session.query(Reserva).filter(Reserva.ReservaID == test_flow.reserva_id).first()
    assert reserva is not None
    assert reserva.RecursoEntregueDono is True


def test_06_confirmar_recepcao_recurso(client, db_session, cookie_residente, test_flow):
    """Um solicitante pode confirmar a recepção do recurso"""
    client.cookies.set("access_token", cookie_residente.get("access_token"))

    response = client.post(
        f"/api/reserva/confirma/rececao/recurso?reserva_id={test_flow.reserva_id}"
    )

    assert response.status_code == 200
    response_data = response.json()
    assert 'Receção do recurso registada com sucesso!' in str(response_data)

    # Verifica se a flag de recepção foi atualizada no banco de dados
    reserva = db_session.query(Reserva).filter(Reserva.ReservaID == test_flow.reserva_id).first()
    assert reserva is not None
    assert reserva.RecursoEntregueVizinho is True


def test_07_confirmar_entrega_caucao(client, db_session, cookie_residente, test_flow):
    """Um solicitante pode confirmar a entrega da caução"""
    client.cookies.set("access_token", cookie_residente.get("access_token"))

    response = client.post(
        f"/api/reserva/confirma/entrega/caucao?reserva_id={test_flow.reserva_id}"
    )

    assert response.status_code == 200
    response_data = response.json()
    assert 'Entrega da caução registada com sucesso!' in str(response_data)

    # Verifica se a flag de caução foi atualizada no banco de dados
    reserva = db_session.query(Reserva).filter(Reserva.ReservaID == test_flow.reserva_id).first()
    assert reserva is not None
    assert reserva.ConfirmarCaucaoVizinho is True


def test_08_confirmar_rececao_caucao(client, db_session, cookie_gestor, test_flow):
    """Um dono do recurso pode confirmar a recepção da caução"""
    client.cookies.set("access_token", cookie_gestor.get("access_token"))

    response = client.post(
        f"/api/reserva/confirma/rececao/caucao?reserva_id={test_flow.reserva_id}"
    )

    assert response.status_code == 200
    response_data = response.json()
    assert 'Receção da caução registada com sucesso!' in str(response_data)

    # Verifica se a flag de caução foi atualizada no banco de dados
    reserva = db_session.query(Reserva).filter(Reserva.ReservaID == test_flow.reserva_id).first()
    assert reserva is not None
    assert reserva.ConfirmarCaucaoDono is True


def test_09_confirmar_bom_estado_devolucao_caucao(client, db_session, cookie_gestor, test_flow):
    """Um dono do recurso pode confirmar o bom estado do produto e devolução da caução"""
    client.cookies.set("access_token", cookie_gestor.get("access_token"))

    response = client.post(
        f"/api/reserva/confirma/bomestado?reserva_id={test_flow.reserva_id}"
    )

    assert response.status_code == 200
    response_data = response.json()
    assert 'Confirmação do bom estado do produto e notificação da devolução da caução registada com sucesso!' in str(response_data)

    # Verifica se as flags foram atualizadas no banco de dados
    reserva = db_session.query(Reserva).filter(Reserva.ReservaID == test_flow.reserva_id).first()
    assert reserva is not None
    assert reserva.DevolucaoCaucao is True
    assert reserva.EstadoRecurso is True


def test_10_submeter_justificativa_mau_estado(client, db_session, cookie_gestor, test_flow):
    """Um dono do recurso pode justificar o mau estado do produto e não devolução da caução"""
    client.cookies.set("access_token", cookie_gestor.get("access_token"))

    justificativa = "Produto com danos na superfície"
    
    response = client.post(
        f"/api/reserva/submissao/justificacao?reserva_id={test_flow.reserva_id}&justificacao={justificativa}"
    )

    assert response.status_code == 200
    response_data = response.json()
    assert 'Justificação registada com sucesso!' in str(response_data)

    # Verifica se a justificativa foi salva no banco de dados
    reserva = db_session.query(Reserva).filter(Reserva.ReservaID == test_flow.reserva_id).first()
    assert reserva is not None
    assert reserva.JustificacaoEstadoProduto == justificativa


def test_11_recusar_pedido_reserva(client, db_session, cookie_gestor, cookie_residente, resource_data):
    """Um dono de recurso pode recusar um pedido de reserva"""
    client.cookies.set("access_token", cookie_residente.get("access_token"))
    
    # Primeiro, cria um novo pedido de reserva para poder recusá-lo
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    day_after_tomorrow = tomorrow + datetime.timedelta(days=1)
    
    pedido_data = {
        "recurso_id": resource_data,  # Assuming resource with ID 1 exists
        "data_inicio": tomorrow.isoformat(),
        "data_fim": day_after_tomorrow.isoformat()
    }
    
    response = client.post(
        "/api/reserva/pedidosreserva/criar",
        data=pedido_data
    )
    
    # Obter o ID do novo pedido para recusá-lo
    pedido = db_session.query(PedidoReserva).order_by(PedidoReserva.PedidoResevaID.desc()).first()
    pedido_id = pedido.PedidoResevaID

    client.cookies.set("access_token", cookie_gestor.get("access_token"))

    # Agora recusa o pedido
    response = client.post(
        f"/api/reserva/pedidosreserva/recusar?pedido_reserva_id={pedido_id}&motivo_recusacao=Recurso indisponível"
    )

    assert response.status_code == 200
    
    # Verifica se o estado do pedido foi alterado para "Rejeitado"
    pedido = db_session.query(PedidoReserva).filter(PedidoReserva.PedidoResevaID == pedido_id).first()
    db_session.refresh(pedido)
    assert pedido is not None
    
    estado = db_session.query(EstadoPedidoReserva).filter(
        EstadoPedidoReserva.EstadoID == pedido.EstadoID
    ).first()
    assert estado is not None
    assert estado.DescEstadoPedidoReserva == "Rejeitado"