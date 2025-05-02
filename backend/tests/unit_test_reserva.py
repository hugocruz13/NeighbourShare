from datetime import datetime
import pytest
from schemas.reserva_schema import PedidoReservaSchemaCreate
from db.session import get_db
from services.reserva_service import cria_pedido_reserva_service


#Coneção com a base de dados
@pytest.fixture
def db_session():
    db = next(get_db())
    yield db

async def test_cria_pedido_reserva_service(db_session):
    #Arrange
    reserva = PedidoReservaSchemaCreate(UtilizadorID=1, RecursoID=1, DataInicio=datetime.date.today(), DataFim=datetime.date.today()+2)

    #Act
    result = await cria_pedido_reserva_service(db_session, reserva)

    #Assert
