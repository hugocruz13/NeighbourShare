from fastapi import APIRouter, Depends, Form
from db.session import get_db
from sqlalchemy.orm import Session
from schemas.recurso_schema import RecursoSchema, DisponibilidadeSchema
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
        db: Session = Depends(get_db)
)
    try:
        recurso_data = RecursoSchema(Nome=nome_recurso,
        DescRecurso=descricao_recurso,
        Caucao=caucao_recurso,
        Disponibilidade_ = DisponibilidadeSchema(DispID= get_disponibilidade_id_service(recurso_disponivel), DescDisponibilidade= recurso_disponivel)

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