from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.models.models import Orcamento
from backend.schemas.orcamento_schema import OrcamentoSchema
import decimal

router = APIRouter(prefix="/orcamentos", tags=["Orcamentos"])

@router.post("/inserir")
async def inserir_orcamento(
        orcamento_data : OrcamentoSchema,
        db:Session = Depends(get_db)
):
    try:
        novo_orcamento = Orcamento(
            Fornecedor=orcamento_data.Fornecedor,
            Valor=orcamento_data.Valor,
            DescOrcamento=orcamento_data.DescOrcamento
        )
        db.add(novo_orcamento)
        db.commit()
        db.refresh(novo_orcamento)

        return {"status": "Novo orçamento inserido com sucesso"}

    except SQLAlchemyError as e:
        db.rollback()
        return {"status": "Erro ao inserir orçamento", "detalhes": str(e)}
