from fastapi import APIRouter, Depends, Form

from db.session import get_db
from sqlalchemy.orm import Session
from schemas.recurso_schema import RecursoSchema
from typing import List
import decimal

from services.recurso_service import *

router = APIRouter(prefix="/recursos", tags=["Recursos"])

@router.post("/inserir")
async def inserir_recurso(
        nome_recurso: str = Form(...),
        descricao_recurso: str = Form(...),
        caucao_recurso: decimal.Decimal = Form(...),
        recurso_disponivel: str = Form(...),
        categoria_recurso: str = Form(...),
        utilizador_recurso: int = Form(...), #TODO Colocar o id do utilizador pelo token
        fotos_recurso: UploadFile = Form(...),
        db: Session = Depends(get_db)
):
    try:
        recurso_data = RecursoSchema(Nome=nome_recurso,
        DescRecurso=descricao_recurso,
        Caucao=caucao_recurso,
        CategoriaID= await get_categoria_id_service(db, categoria_recurso),
        DisponibilidadeID = await get_disponibilidade_id_service(db, recurso_disponivel),
        UtilizadorID = utilizador_recurso)

        sucesso, msg = await inserir_recurso_service(db, recurso_data, fotos_recurso)

        if sucesso:
            return {"message": "Recurso inserido com sucesso"}
        else:
            raise HTTPException(status_code=400, detail=msg)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[RecursoSchema])
async def listar_recursos(
        db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os recursos
    """
    return await lista_recursos_service(db)

@router.get("/disponiveis", response_model=List[RecursoSchema])
async def listar_recursos_disponiveis(
    db:Session = Depends(get_db)
):
    """
    Endpoint para consultar os recursos disponíveis (ID Disponibilidade = 1)
    """
    return await lista_recursos_disponiveis_service(db)

@router.get("/indisponiveis", response_model=List[RecursoSchema])
async def listar_recursos_indisponiveis(
    db:Session = Depends(get_db)
):
    """
    Endpoint para consultar os recursos indisponíveis (ID Disponibilidade = 2)
    """
    return await lista_recursos_indisponiveis_service(db)