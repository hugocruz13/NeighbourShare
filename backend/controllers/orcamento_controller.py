from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.schemas.orcamento_schema import OrcamentoSchema
import backend.services.orcamento_service as orcamento_service

router = APIRouter(prefix="/orcamentos", tags=["Orcamentos"])

# Inserir um orçamento
@router.post("/inserir")
async def inserir_orcamento(orcamento: OrcamentoSchema, db: Session = Depends(get_db)):
    try:
        sucesso, msg = await orcamento_service.inserir_orcamento_service(db, orcamento)
        if sucesso:
            return {"message": "Orçamento inserido com sucesso"}
        else:
            raise HTTPException(status_code=400, detail=msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
