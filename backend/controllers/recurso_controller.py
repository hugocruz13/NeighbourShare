from fastapi import APIRouter, Depends
from backend.db.session import get_db
from sqlalchemy.orm import Session
from typing import List
from backend.schemas.recurso_schema import RecursoSchema
from typing import Union, Dict, List
from pydantic import BaseModel

from backend.services.recurso_service import *

router = APIRouter(prefix="/recursos", tags=["Recursos"])

class ResponseModelTuple(BaseModel):
    success: bool
    data: Dict[str, str]

ResponseModel = Union[ResponseModelTuple, List[RecursoSchema]]

@router.get("/", response_model=ResponseModel)
def listar_recursos(
        db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os recursos
    """
    return lista_recursos_service(db)

@router.get("/disponiveis", response_model=ResponseModel)
def listar_recursos_disponiveis(
    db:Session = Depends(get_db)
):
    """
    Endpoint para consultar os recursos disponíveis (ID Disponibilidade = 1)
    """
    return lista_recursos_disponiveis_service(db)

@router.get("/indisponiveis", response_model=ResponseModel)
def listar_recursos_indisponiveis(
    db:Session = Depends(get_db)
):
    """
    Endpoint para consultar os recursos indisponíveis (ID Disponibilidade = 2)
    """
    return lista_recursos_indisponiveis_service(db)