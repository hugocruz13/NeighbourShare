from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.models import Orcamento, EntidadeExterna, PedidoManutencao
from schemas.orcamento_schema import OrcamentoSchema, OrcamentoUpdateSchema, TipoOrcamento
from sqlalchemy.exc import SQLAlchemyError
from db.repository.recurso_comum_repo import obter_pedido_manutencao_db, obter_pedido_novo_recurso_db

#Inserção de um novo orçamento na base de dados
async def inserir_orcamento_db(db: Session, orcamento: OrcamentoSchema):
    try:
        novo_orcamento = Orcamento(
            EntidadeExternaEntidadeID=orcamento.IDEntidade,
            Valor=orcamento.Valor,
            DescOrcamento=orcamento.DescOrcamento,
            NomePDF = orcamento.NomePDF)

        if orcamento.TipoProcesso == TipoOrcamento.MANUTENCAO:
            pedido_manutencao = await obter_pedido_manutencao_db(db, orcamento.IDProcesso)
            if pedido_manutencao :
                novo_orcamento.PedidoManutencao.append(pedido_manutencao)
            else:
                raise HTTPException(status_code=400, detail="Pedido de mantenção não existe")
        else:
            pedido_novo_recurso = await obter_pedido_novo_recurso_db(db, orcamento.IDProcesso)
            if pedido_novo_recurso :
                novo_orcamento.PedidoNovoRecurso.append(pedido_novo_recurso)
            else:
                raise HTTPException(status_code=400, detail="Pedido de mantenção não existe")
        db.add(novo_orcamento)
        db.commit()
        db.refresh(novo_orcamento)
        return novo_orcamento.OrcamentoID, {'message': 'Inserção do orçamento realizada com sucesso!'}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Listagem dos orçamentos registados na base de dados
async def listar_orcamentos_db(db: Session):
    try:
        orcamentos = db.query(Orcamento).all()
        return orcamentos
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Eliminar um orçamento da base de dados
async def eliminar_orcamento_db(db: Session, orcamento_id: int):
    try:
        orcamento = db.query(Orcamento).get(orcamento_id)
        if not orcamento:
            return False, {'erro': 'Orçamento não encontrado'}

        # Remover associação com PedidoManutencao
        for pedido in orcamento.PedidoManutencao:
            pedido.Orcamento_.remove(orcamento)

        # Remover associação com PedidoNovoRecurso
        for pedido in orcamento.PedidoNovoRecurso:
            pedido.Orcamento_.remove(orcamento)

        # Eliminar o orçamento da base de dados
        db.delete(orcamento)
        db.commit()
        return True, {'mensagem': 'Orçamento removido com sucesso!'}

        return True, {'Orcamento removido com sucesso!'}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Altera os dados de um determinado orçamento
async def altera_orcamento_db(db:Session, orcamento:OrcamentoUpdateSchema, nomepdf:str):
    try:
        if nomepdf: #Se for adicionado um novo pdf
            db.query(Orcamento).filter(Orcamento.OrcamentoID == orcamento.OrcamentoID).update(
                {Orcamento.EntidadeExternaEntidadeID: orcamento.IDEntidade,
                 Orcamento.Valor: orcamento.Valor,
                 Orcamento.DescOrcamento: orcamento.DescOrcamento,
                 Orcamento.NomePDF: nomepdf}
            )
        else: # Se não for adicionado, mantêm o pdf antigo
            db.query(Orcamento).filter(Orcamento.OrcamentoID == orcamento.OrcamentoID).update(
                {Orcamento.EntidadeExternaEntidadeID: orcamento.IDEntidade,
                 Orcamento.Valor: orcamento.Valor,
                 Orcamento.DescOrcamento: orcamento.DescOrcamento
                 }
            )
        db.commit()
        return True, {'Orcamento atualizado com sucesso!'}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Tras o orcamento
async def get_orcamento_by_id(db: Session, orcamento_id: int):
    try:
        orcamento = db.query(Orcamento).filter(Orcamento.OrcamentoID == orcamento_id).first()
        return orcamento
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Metedo APENAS para teste
async def get_last_id(db:Session):
    try:
        orcamento = db.query(Orcamento).order_by(Orcamento.OrcamentoID.desc()).first()
        return orcamento
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))
