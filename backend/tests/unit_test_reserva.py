from datetime import datetime, timedelta
from fastapi import HTTPException
import pytest
from db.models import Reserva
from schemas.reserva_schema import PedidoReservaSchemaCreate, PedidoReservaEstadosSchema, ReservaSchemaCreate
from db.session import get_db
from services.reserva_service import cria_pedido_reserva_service, muda_estado_pedido_reserva_service, \
    cria_reserva_service, get_reserva_service, lista_reservas_service, lista_pedidos_reserva_service, \
    confirma_entrega_recurso_service, confirma_entrega_caucao_service, inserir_justificacao_caucao_service, \
    inserir_bom_estado_produto_e_devolucao_caucao


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


async def test_cria_pedido_reserva_service_erro(db_session):
    # Arrange
    reserva = PedidoReservaSchemaCreate(
        UtilizadorID=1,
        RecursoID=999,
        DataInicio=(datetime.today() + timedelta(days=1)).date(),
        DataFim=(datetime.today() + timedelta(days=3)).date())

    # Act
    with pytest.raises(HTTPException) as exc_info:
        await cria_pedido_reserva_service(db_session, reserva)

    # Assert
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Recurso não existe"

async def test_muda_estado_pedido_reserva_service(db_session):
    # Arrange
    id_pedido = 12
    motivo = "Quero fazer um teste"
    estado = PedidoReservaEstadosSchema.APROVADO
    #Act
    result =await muda_estado_pedido_reserva_service(db_session,id_pedido,estado,motivo)

    #Assert
    assert result[0]=={'Estado do pedido de reserva alterado com sucesso!'}

async def test_cria_reserva_service(db_session):
    # Arrange
    reserva = ReservaSchemaCreate(PedidoReservaID=12)
    #Act
    result =await cria_reserva_service(db_session,reserva)

    #Assert
    assert result[0]=={'Reserva criada com sucesso!'}
    assert result[1] == {'Estado do pedido de reserva alterado com sucesso!'}

async def test_cria_reserva_service_erro(db_session):
    # Arrange
    reserva = ReservaSchemaCreate(PedidoReservaID=50)
    #Act
    with pytest.raises(HTTPException) as exc_info:
        await cria_reserva_service(db_session,reserva)

    #Assert
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Pedido de reserva não existe"

async def test_get_reserva_service(db_session):
    # Arrange
    id_reserva = 12
    #Act
    result = await get_reserva_service(db_session, id_reserva)

    # Assert
    assert isinstance(result, Reserva)

async def test_get_reserva_service_erro(db_session):
    # Arrange
    id_reserva = 2000
    # Act
    with pytest.raises(HTTPException) as exc_info:
        await get_reserva_service(db_session, id_reserva)

    # Assert
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Reserva não existe!"

async def test_lista_reservas_service(db_session):
    # Arrange
    user_id = 1
    # Act
    lista = await lista_reservas_service(db_session,user_id)
    # Assert
    assert isinstance(lista, tuple)

async def test_lista_reservas_service_erro(db_session):
    # Arrange
    user_id = 600
    # Act
    with pytest.raises(HTTPException) as exc_info:
        await lista_reservas_service(db_session,user_id)
    # Assert
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Nenhuma reserva encontrada"

async def test_lista_pedidos_reserva_service(db_session):
    # Arrange
    user_id = 1
    # Act
    lista = await lista_pedidos_reserva_service(db_session,user_id)
    # Assert
    assert isinstance(lista, tuple)

async def test_lista_pedidos_reserva_service_erro(db_session):
    # Arrange
    user_id = 500
    # Act
    with pytest.raises(HTTPException) as exc_info:
        await lista_reservas_service(db_session,user_id)
    # Assert
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Nenhuma reserva encontrada"

async def test_confirma_entrega_recurso_service(db_session):
    # Arrange
    reserva_id = 3
    # Act
    resultado = await confirma_entrega_recurso_service(db_session, reserva_id)
    # Assert
    assert resultado == {'Entrega do produto registada com sucesso!'}


async def test_confirma_entrega_recurso_service_erro(db_session):
    # Arrange
    reserva_id = 30
    # Act
    with pytest.raises(HTTPException) as exc_info:
        await confirma_entrega_recurso_service(db_session,reserva_id)
    # Assert
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Reserva não existe!"

async def test_confirma_entrega_caucao_service(db_session):
    # Arrange
    reserva_id = 3
    # Act
    resultado = await confirma_entrega_caucao_service(db_session, reserva_id)
    # Assert
    assert resultado == {'Entrega da caução registada com sucesso!'}


async def test_confirma_entrega_caucao_service_erro(db_session):
    # Arrange
    reserva_id = 30
    # Act
    with pytest.raises(HTTPException) as exc_info:
        await confirma_entrega_recurso_service(db_session,reserva_id)
    # Assert
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Reserva não existe!"

async def test_inserir_justificacao_caucao_service(db_session):
    # Arrange
    reserva_id = 3
    just = "Testar"
    # Act
    resultado = await inserir_justificacao_caucao_service(db_session, reserva_id,just)
    # Assert
    assert resultado[0] == {'Justificação registada com sucesso!'}

async def test_inserir_justificacao_caucao_service_erro(db_session):
    # Arrange
    reserva_id = 30
    just = "Testar"
    # Act
    with pytest.raises(HTTPException) as exc_info:
        await inserir_justificacao_caucao_service(db_session,reserva_id,just)
    # Assert
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Reserva não existe!"

async def test_inserir_bom_estado_produto_e_devolucao_caucao(db_session):
    # Arrange
    reserva_id = 3
    # Act
    resultado = await inserir_bom_estado_produto_e_devolucao_caucao(db_session, reserva_id)
    # Assert
    assert resultado[0] == {'Confirmação do bom estado do produto e notificação da devolução da caução registada com sucesso!'}

async def test_inserir_bom_estado_produto_e_devolucao_caucao_erro(db_session):
    # Arrange
    reserva_id = 30

    # Act
    with pytest.raises(HTTPException) as exc_info:
        await inserir_bom_estado_produto_e_devolucao_caucao(db_session,reserva_id)
    # Assert
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Reserva não existe!"