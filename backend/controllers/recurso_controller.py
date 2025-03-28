from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from backend.db.session import get_db
from backend.models.models import Recurso
from backend.schemas.recurso_schema import RecursoSchema

router = APIRouter(prefix="/recursos", tags=["Recursos"])

@router.get("/", response_model=List[RecursoSchema])
def listar_recursos(
        db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os recursos
    """
    recursos = (
        db.query(Recurso)
        .options(
            joinedload(Recurso.Utilizador_),
            joinedload(Recurso.Categoria_),
            joinedload(Recurso.Disponibilidade_)
        )
        .all()
    )

    if not recursos:
        raise HTTPException(status_code=404, detail="Nenhum recurso encontrado")

    return recursos
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
        .options(
            joinedload(Recurso.Utilizador_),
            joinedload(Recurso.Categoria_),
            joinedload(Recurso.Disponibilidade_)
        )
        .all()
    )

    if not recursos_disponiveis:
        raise HTTPException(status_code=404, detail="Nenhum recurso disponível encontrado")

    return recursos_disponiveis

@router.get("/indisponiveis", response_model=List[RecursoSchema])
def listar_recursos_indisponiveis(
    db:Session = Depends(get_db)
):
    """
    Endpoint para consultar os recursos indisponíveis (ID Disponibilidade = 2)
    """
    recursos_indisponiveis = (
        db.query(Recurso)
        .filter(Recurso.DispID == 2)
        .options(
            joinedload(Recurso.Utilizador_),
            joinedload(Recurso.Categoria_),
            joinedload(Recurso.Disponibilidade_)
        )
        .all()
    )

    if not recursos_indisponiveis:
        raise HTTPException(status_code=404, detail="Nenhum recurso indisponível encontrado")

    return recursos_indisponiveis