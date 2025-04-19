from sqlalchemy.orm import Session
from db.models import Orcamento
from schemas.orcamento_schema import OrcamentoSchema, OrcamentoUpdateSchema, TipoOrcamento
from sqlalchemy.exc import SQLAlchemyError
from db.repository.recurso_comum_repo import obter_pedido_manutencao_db, obter_pedido_novo_recurso_db

#Inserção de um novo orçamento na base de dados
async def inserir_orcamento_db(db: Session, orcamento: OrcamentoSchema):
    try:
        novo_orcamento = Orcamento(
            Fornecedor=orcamento.Fornecedor,
            Valor=orcamento.Valor,
            DescOrcamento=orcamento.DescOrcamento,
            NomePDF = orcamento.NomePDF
        )

        if orcamento.TipoProcesso == TipoOrcamento.MANUTENCAO:
            pedido_manutencao = await obter_pedido_manutencao_db(db, orcamento.IDProcesso)
            novo_orcamento.Manutencao.append(pedido_manutencao)
        else:
            pedido_novo_recurso = await obter_pedido_novo_recurso_db(db, orcamento.IDProcesso)
            novo_orcamento.PedidoNovoRecurso.append(pedido_novo_recurso)

        db.add(novo_orcamento)
        db.commit()
        db.refresh(novo_orcamento)



        return novo_orcamento.OrcamentoID, {'Inserção do orçamento realizada com sucesso!'}

    except SQLAlchemyError as e:
        db.rollback()
        return False, {'details': str(e)}

#Listagem dos orçamentos registados na base de dados
async def listar_orcamentos_db(db: Session):
    try:
        orcamentos = db.query(Orcamento).all()
        return orcamentos
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

#Eliminar um orçamento da base de dados
async def eliminar_orcamento_db(db: Session, orcamento_id: int):
    try:
        db.query(Orcamento).filter(Orcamento.OrcamentoID == orcamento_id).delete()
        db.commit()
        return True, {'Orcamento removido com sucesso!'}
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

#Altera os dados de um determinado orçamento
async def altera_orcamento_db(db:Session, orcamento:OrcamentoUpdateSchema, nomepdf:str):
    try:
        if nomepdf: #Se for adicionado um novo pdf
            db.query(Orcamento).filter(Orcamento.OrcamentoID == orcamento.OrcamentoID).update(
                {Orcamento.Fornecedor: orcamento.Fornecedor,
                 Orcamento.Valor: orcamento.Valor,
                 Orcamento.DescOrcamento: orcamento.DescOrcamento,
                 Orcamento.NomePDF: nomepdf}
            )
        else: # Se não for adicionado, mantêm o pdf antigo
            db.query(Orcamento).filter(Orcamento.OrcamentoID == orcamento.OrcamentoID).update(
                {Orcamento.Fornecedor: orcamento.Fornecedor,
                 Orcamento.Valor: orcamento.Valor,
                 Orcamento.DescOrcamento: orcamento.DescOrcamento
                 }
            )
        db.commit()
        return True, {'Orcamento atualizado com sucesso!'}
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))
