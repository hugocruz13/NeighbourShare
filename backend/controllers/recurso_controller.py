from fastapi import APIRouter, Depends
from db.session import get_db
from sqlalchemy.orm import Session
from schemas.recurso_schema import RecursoSchema
from typing import List
from services.recurso_service import *
from middleware.auth_middleware import role_required
from schemas.user_schemas import UserJWT

router = APIRouter(prefix="/recursos", tags=["Recursos"])

@router.get("/", response_model=List[RecursoSchema])
async def listar_recursos(
        db:Session = Depends(get_db),
        token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))
):
    """
    Endpoint para consultar todos os recursos
    """
    return await lista_recursos_service(db)

@router.get("/disponiveis", response_model=List[RecursoSchema])
async def listar_recursos_disponiveis(
    db:Session = Depends(get_db),
    token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))
):
    """
    Endpoint para consultar os recursos disponíveis (ID Disponibilidade = 1)
    """
    return await lista_recursos_disponiveis_service(db)

@router.get("/indisponiveis", response_model=List[RecursoSchema])
async def listar_recursos_indisponiveis(
    db:Session = Depends(get_db),
    token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))
):
    """
    Endpoint para consultar os recursos indisponíveis (ID Disponibilidade = 2)
    """
    return await lista_recursos_indisponiveis_service(db)