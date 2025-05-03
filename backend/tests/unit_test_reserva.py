from datetime import datetime, timedelta
from http.client import HTTPException

import pytest
from dns import exception

from schemas.reserva_schema import PedidoReservaSchemaCreate, PedidoReservaEstadosSchema
from db.session import get_db
from services.reserva_service import cria_pedido_reserva_service, lista_pedidos_reserva_ativos_service, \
    muda_estado_pedido_reserva_service, get_reserva_service


#Coneção com a base de dados
@pytest.fixture
def db_session():
    db = next(get_db())
    yield db

async def test_cria_pedido_reserva_service(db_session):
    # Arrange
    reserva = PedidoReservaSchemaCreate(
        UtilizadorID=1,
        RecursoID=4,
        DataInicio=(datetime.today() + timedelta(days=1)).date(),
        DataFim=(datetime.today() + timedelta(days=3)).date())
    #Act
    result = await cria_pedido_reserva_service(db_session,reserva)

    #Assert
    assert result[0] == {'Pedido de reserva criado com sucesso!'}
    assert result[1] == {'Inserção de nova notifcação realizada com sucesso!'}

async def test_cria_pedido_reserva_service_erro(db_session):
    # Arrange
    reserva = PedidoReservaSchemaCreate(
        UtilizadorID=1,
        RecursoID=999,
        DataInicio=(datetime.today() + timedelta(days=1)).date(),
        DataFim=(datetime.today() + timedelta(days=3)).date())
    #Act
    with pytest.raises(HTTPException) as exc_info:
        await cria_pedido_reserva_service(db_session,reserva)

    #Assert
    assert exc_info.value.status_code == 400
    assert "FOREIGN KEY constraint" in exc_info.value.detail

async def test_lista_pedidos_reserva_ativos_service(db_session):
    #Act
    lista = lista_pedidos_reserva_ativos_service(db_session)

    #Assert
    assert isinstance(lista, list)

async def test_muda_estado_pedido_reserva_service(db_session):
    # Arrange
    reserva = 5
    #Act
    result = await get_reserva_service(db_session,reserva)
    #Assert
    assert isinstance(result, tuple)
    assert result[0] == {'Estado do pedido de reserva alterado com sucesso!'}
