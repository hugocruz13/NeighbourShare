from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.db.session import get_db
from backend.db.models import Recurso
from backend.schemas.recurso_schema import RecursoSchema

router = APIRouter(prefix="/recursos", tags=["Recursos"])

@router.get("/disponiveis", response_model=List[RecursoSchema])
def listar_recursos_disponiveis(
    db:Session = Depends(get_db)
):
    """
    Endpoint para consultar os recursos disponíveis (ID Disponibilidade = 1)
    """
    recursos_disponiveis = (
        db.query(Recurso)
        .filter(Recurso.DispID == 1)
        .all()
    )

    if not recursos_disponiveis:
        raise HTTPException(status_code=404, detail="Nenhum recurso disponível encontrado")

    return recursos_disponiveis