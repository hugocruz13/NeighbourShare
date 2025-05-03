import pytest
from fastapi import HTTPException, UploadFile

import db
from db.models import Utilizador
from services.auth_service import (
    get_user_data,
    registar_utilizador,
    atualizar_novo_utilizador,
    guardar_imagem,
    user_auth,
    eliminar_utilizador,
    atualizar_utilizador,
)
from schemas.user_schemas import (
    UserLogin, UserRegistar, UserUpdateInfo, UserJWT, NewUserUpdate, ResetPassword
)
import random, string, datetime

@pytest.fixture
def db_session():
    from db.session import get_db
    return next(get_db())

@pytest.fixture
def new_user_para_delete(db_session):
    data = datetime.date.today()
    new_user = Utilizador(NomeUtilizador="none", DataNasc=data, Email="paradelete@pt.pt", Contacto=000000000, PasswordHash="none",
                          Salt="none", TUID=1, Verificado=True, Path="none")
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    return new_user

@pytest.fixture
def new_user_para_update(db_session):
    data = datetime.date.today()
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    new_user = Utilizador(NomeUtilizador="none", DataNasc=data, Email=f"{random_string}@pt.pt", Contacto=000000000, PasswordHash="none",
                          Salt="none", TUID=1, Verificado=True, Path="none")
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    return new_user

# get_user_data
async def test_get_user_data_sucesso(db_session):
    resultado = await get_user_data(db_session, 1)  # use id válido conforme base de testes
    assert resultado is not None

# registar_utilizador
async def test_registar_utilizador_simples(db_session):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    user = UserRegistar(email=f"{random_string}@teste.pt", password="12Senha#@!", role="residente")
    res, msg = await registar_utilizador(user, db_session)
    assert res is True

async def test_registar_utilizador_repetido(db_session):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    user = UserRegistar(email=f"{random_string}@teste.pt", password="Senha456!@", role="residente")
    await registar_utilizador(user, db_session)
    res, msg = await registar_utilizador(user, db_session)
    assert res is False
    assert "Email registado" in msg

# guardar_imagem
async def test_guardar_imagem_ok():
    class DummyUpload:
        content_type = 'image/jpeg'
        filename = "testeimg.jpg"
        file = open(__file__, "rb")
    imagem = DummyUpload()
    from os import environ
    environ["UPLOAD_DIR_PERFIL"] = "."
    environ["SAVE_PERFIL"] = "."
    path = await guardar_imagem(imagem, 999)
    assert "testeimg.jpg" in path

async def test_guardar_imagem_tipo_invalido():
    class DummyUpload:
        content_type = 'application/pdf'
        filename = "file.pdf"
        file = open(__file__, "rb")
    imagem = DummyUpload()
    from os import environ
    environ["UPLOAD_DIR_PERFIL"] = "."
    environ["SAVE_PERFIL"] = "."
    with pytest.raises(HTTPException):
        await guardar_imagem(imagem, 1001)

# user_auth
async def test_user_auth_ok(db_session):
    user_login = UserLogin(email="admin@email.com", password="admin")
    res = await user_auth(db_session, user_login)
    assert res is not None

async def test_user_auth_naoverificado(db_session):
    # 1º criar utilizador
    with pytest.raises(HTTPException):
        user = UserRegistar(email="teste.login@pt.pt", password="Teste123!#", role="residente")
        await registar_utilizador(user, db_session)
        user_login = UserLogin(email="teste.login@pt.pt", password="Teste123!#")
        res = await user_auth(db_session, user_login)

async def test_user_auth_incorreto(db_session):
    user_login = UserLogin(email="naoexiste@pt.pt", password="errada")
    with pytest.raises(HTTPException):
        await user_auth(db_session, user_login)

# eliminar_utilizador
async def test_eliminar_utilizador_ok(db_session, new_user_para_delete):
    res = await eliminar_utilizador(db_session, "paradelete@pt.pt")
    assert res is True or res is not None

async def test_eliminar_utilizador_erro(db_session):
    with pytest.raises(HTTPException):
        await eliminar_utilizador(db_session, "inexistente@pt.pt")

# 10. atualizar_utilizador
async def test_atualizar_utilizador_ok(db_session, new_user_para_update):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    user_info = UserUpdateInfo(
        nome=f"{random_string}",
        data_nascimento=datetime.date(1990, 1, 1),
        contacto=123456789,
    )
    resultado = await atualizar_utilizador(db_session, new_user_para_update.UtilizadorID, user_info)
    assert resultado is not None
    user_verify = db_session.query(Utilizador).filter(Utilizador.UtilizadorID == new_user_para_update.UtilizadorID).first()
    assert user_verify.NomeUtilizador == f"{random_string}"
    assert user_verify.DataNasc == datetime.date(1990, 1, 1)
    assert user_verify.Contacto == 123456789

async def test_atualizar_utilizador_fail(db_session):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    user_info = UserUpdateInfo(
        nome=f"{random_string}",
        data_nascimento=datetime.date(1990, 1, 1),
        contacto=123456789,
    )
    val = await atualizar_utilizador(db_session, -1, user_info)
    assert val is False