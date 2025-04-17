from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.orcamento_schema import OrcamentoSchema
import services.orcamento_service as orcamento_service
import decimal

router = APIRouter(prefix="/orcamentos", tags=["Orcamentos"])

# Inserir um orçamento
@router.post("/inserir")
async def inserir_orcamento(
        fornecedor_orcamento : str = Form(...),
        valor_orcamento : decimal.Decimal = Form(...),
        descricao_orcamento: str = Form(...),
        pdforcamento: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    try:
        orcamento_data = OrcamentoSchema(Fornecedor=fornecedor_orcamento,DescOrcamento=descricao_orcamento, Valor=valor_orcamento, NomePDF=pdforcamento.filename)

        sucesso, msg = await orcamento_service.inserir_orcamento_service(db, orcamento_data, pdforcamento)

        if sucesso:
            return {"message": "Orçamento inserido com sucesso"}
        else:
            raise HTTPException(status_code=400, detail=msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
