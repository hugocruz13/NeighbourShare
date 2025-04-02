import db.repository.recurso_repo as recurso_repo
import db.session as session
from fastapi import HTTPException

async def lista_recursos_service(db:session):

    lista_recursos = await recurso_repo.listar_recursos_db(db)

    if not lista_recursos:
        raise HTTPException(status_code=400, detail="Nenhum recurso encontrado")

    return lista_recursos

async def lista_recursos_disponiveis_service(db:session):

    lista_recursos_disponiveis = await recurso_repo.listar_recursos_disponiveis_db(db)

    if not lista_recursos_disponiveis:
        raise HTTPException(status_code=400, detail="Nenhum recurso disponivel encontrado")

    return lista_recursos_disponiveis

async def lista_recursos_indisponiveis_service(db:session):

    lista_recursos_indisponiveis = await recurso_repo.listar_recursos_indisponiveis(db)

    if not lista_recursos_indisponiveis:
        raise HTTPException(status_code=400, detail="Nenhum recurso indisponivel encontrado")

    return lista_recursos_indisponiveis