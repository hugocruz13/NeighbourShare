import pytest
from fastapi import HTTPException

from db.models import EntidadeExterna
from db.repository.entidade_repo import inserir_entidade_testes
from db.session import get_db
from schemas.entidade_schema import EntidadeSchema, EntidadeUpdateSchema
from services.entidade_service import registar_entidade, ver_entidades, eliminar_entidade_service,  update_entidade_service
from pydantic import ValidationError

#Conexão com a base de dados
@pytest.fixture
def db_session():
    db = next(get_db())
    yield db

async def test_registar_entidade(db_session):
    #Arrange
    entidade = EntidadeSchema(Especialidade="Vasco", Contacto=253787945, Email="vasco@empresa.pt", Nome="empresa", Nif=123456789)

    #Act
    registo = await registar_entidade(entidade, db_session)

    #Assert
    assert registo[0]==True
    assert registo[1]=={'Nova entidade inserida com sucesso.'}


async def test_registar_entidade_schema(db_session):
    # Arrange & Assert
    with pytest.raises(ValidationError) as exc_info:
        EntidadeSchema(
            Especialidade="Vasco",
            Contacto=253787945,
            Email="vasco@empresa.pt",
            Nome="empresa",
            Nif=9999999999  # 10 dígitos — inválido
        )

    # Opcional: confirmar que o erro é mesmo do Nif
    errors = exc_info.value.errors()
    assert any(error['loc'] == ('Nif',) for error in errors)

async def test_ver_entidades(db_session):
    #Act
    lista = await ver_entidades(db_session)

    #Assert
    assert isinstance(lista, list)

async def test_eliminar_entidade_service(db_session):
    # Arrange(ajustar id)
    entidade =await inserir_entidade_testes(db_session, EntidadeExterna(Especialidade="Elevadores", Contacto=253787945,Email="teste@teste.com",Nome="Elevadores", Nif=123456789))

    #Act
    test = await eliminar_entidade_service(entidade.EntidadeID, db_session)

    #Assert
    assert test[0]==True

@pytest.mark.asyncio
async def test_eliminar_entidade_service_erro(db_session):
    # Arrange
    id_entidade = 5000

    # Act + Assert
    with pytest.raises(HTTPException) as exc_info:
        await eliminar_entidade_service(id_entidade, db_session)

    # Assert
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Entidade não existe"

async def test_update_entidade_service(db_session):
    # Arrange
    entidade =await inserir_entidade_testes(db_session, EntidadeExterna(Especialidade="Elevadores", Contacto=253787945,Email="teste@teste.com",Nome="Elevadores", Nif=123456789))
    entidade_teste = EntidadeUpdateSchema(EntidadeID=entidade.EntidadeID,Especialidade="Carros",Contacto=253945787,Email="carros@teste.com",Nome="Carrps",Nif=678912345)
    #Act
    test = await update_entidade_service(entidade_teste, db_session)

    #Assert
    assert test[0]==True