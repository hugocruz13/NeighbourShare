from sqlalchemy.orm import Session
from db.models import Orcamento
from schemas.orcamento_schema import OrcamentoSchema
from sqlalchemy.exc import SQLAlchemyError

async def inserir_orcamento_db(db: Session, orcamento: OrcamentoSchema):
    try:
        novo_orcamento = Orcamento(
            Fornecedor=orcamento.Fornecedor,
            Valor=orcamento.Valor,
            DescOrcamento=orcamento.DescOrcamento
        )
        db.add(novo_orcamento)
        db.commit()
        db.refresh(novo_orcamento)

        return True, {'Inserção do orçamento realizada com sucesso!'}

    except SQLAlchemyError as e:
        db.rollback()
        return False, {'details': str(e)}