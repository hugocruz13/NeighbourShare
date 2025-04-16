from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException
from middleware.auth_middleware import *
from db.session import get_db
from sqlalchemy.orm import Session
from schemas.recurso_schema import *
from typing import List
import decimal

from schemas.user_schemas import UserJWT
from services.recurso_service import *

router = APIRouter(prefix="/recursos", tags=["Recursos"])

@router.post("/inserir")
async def inserir_recurso(
        token : UserJWT = Depends(jwt_middleware),
        nome_recurso: str = Form(...),
        descricao_recurso: str = Form(...),
        caucao_recurso: decimal.Decimal = Form(...),
        recurso_disponivel: str = Form(...),
        categoria_recurso: str = Form(...),
        fotos_recurso: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    try:
        recurso_data = RecursoInserirSchema(Nome=nome_recurso,
        DescRecurso= descricao_recurso,
        Caucao= caucao_recurso,
        CatID= await get_categoria_id_service(db, categoria_recurso),
        DispID = await get_disponibilidade_id_service(db, recurso_disponivel),
        UtilizadorID = token.id)

        sucesso, msg = await inserir_recurso_service(db, recurso_data, fotos_recurso)

        if sucesso:
            return {"message": "Recurso inserido com sucesso"}
        else:
            raise HTTPException(status_code=400, detail=msg)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#Lista todos os recursos registados
@router.get("/", response_model=List[RecursoGetTodosSchema])
async def listar_recursos(
        db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os recursos
    """
    return await lista_recursos_service(db)

#Lista os recursos de um utilizador
@router.get("/pessoais", response_model=List[RecursoGetUtilizadorSchema])
async def listar_recursos_pessoais(
        token: UserJWT = Depends(jwt_middleware),
        db:Session = Depends(get_db)
):
    return await lista_recursos_utilizador_service(db, token.id)

#Lista todos os recursos disponíveis
@router.get("/disponiveis", response_model=List[RecursoGetTodosSchema])
async def listar_recursos_disponiveis(
    db:Session = Depends(get_db)
):
    """
    Endpoint para consultar os recursos disponíveis (ID Disponibilidade = 1)
    """
    return await lista_recursos_disponiveis_service(db)

#Lista todos os recursos indisponíveis
@router.get("/indisponiveis", response_model=List[RecursoGetTodosSchema])
async def listar_recursos_indisponiveis(
    db:Session = Depends(get_db)
):
    """
    Endpoint para consultar os recursos indisponíveis (ID Disponibilidade = 2)
    """
    return await lista_recursos_indisponiveis_service(db)

@router.get("/{recurso_id}", response_model=RecursoGetTodosSchema)
async def listar_recurso(
        recurso_id: int,
        db:Session = Depends(get_db)
):
    return await lista_recurso_service(db, recurso_id)
