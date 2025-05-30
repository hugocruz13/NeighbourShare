from datetime import datetime, date, timedelta
from http.client import HTTPException

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from schemas.votacao_schema import Criar_Votacao, Votar_id, Consulta_Votacao, Votacao_Return, TipoVotacaoPedidoNovoRecurso, TipoVotacao
from db.models import Votacao, PedidoNovoRecurso, PedidoManutencao, Voto, Orcamento, VotacaoPedidoNovoRecurso


async def criar_votacao_nr_db(db: Session, votacao: Criar_Votacao, tipovotacao:TipoVotacaoPedidoNovoRecurso):
    try:
        votacao_new = Votacao(Titulo=votacao.titulo, Descricao=votacao.descricao, DataInicio=date.today(), DataFim= votacao.data_fim, Processada=False)
        db.add(votacao_new)
        db.commit()
        pedido = db.query(PedidoNovoRecurso).filter(PedidoNovoRecurso.PedidoNovoRecID == votacao.id_processo).first()
        if not pedido:
            raise RuntimeError(f"Pedido com ID {votacao.id_processo} não encontrado.")

        votacao_pedido_novo_recurso = VotacaoPedidoNovoRecurso(VotacaoID=votacao_new.VotacaoID, PedidoNovoRecID=pedido.PedidoNovoRecID, TipoVotacao=tipovotacao.value)
        db.add(votacao_pedido_novo_recurso)
        db.commit()

        return Votacao_Return(id_votacao=votacao_new.VotacaoID, data_inicio=votacao_new.DataInicio, data_fim=votacao_new.DataFim, processada=False)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def criar_votacao_pedido_manutencao_db(db: Session, votacao: Criar_Votacao):
    try:
        votacao_new = Votacao(Titulo=votacao.titulo, Descricao=votacao.descricao, DataInicio=date.today(), DataFim= votacao.data_fim, Processada=False)
        pedido_manutencao = db.query(PedidoManutencao).filter(PedidoManutencao.PMID == votacao.id_processo).first()

        if not pedido_manutencao:
            raise RuntimeError(f"Manutenção com ID {votacao.id_processo} não encontrado.")

        db.add(votacao_new)
        db.commit()
        db.refresh(votacao_new)

        pedido_manutencao.VotacaoID = votacao_new.VotacaoID
        db.commit()

        return Votacao_Return(id_votacao=votacao_new.VotacaoID, data_inicio=votacao_new.DataInicio, data_fim=votacao_new.DataFim, processada=False)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def registar_voto(db: Session, voto:Votar_id):
    try:
        voto_new = Voto(VotacaoID=voto.id_votacao, UtilizadorID=voto.id_user, EscolhaVoto=voto.voto, DataVoto=datetime.today())
        db.add(voto_new)
        db.commit()
        db.refresh(voto_new)
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def existe_nr(db: Session, id:int):
    try:
        query = db.query(PedidoNovoRecurso).filter(PedidoNovoRecurso.PedidoNovoRecID == id).first()
        if query:
            return True, query.EstadoPedNovoRecID
        else:
            return False, "none"
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def existe_pedido_manutencao(db: Session, id:int):
    try:
        query = db.query(PedidoManutencao).filter(PedidoManutencao.PMID == id).first()
        return True if query else False
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def existe_votacao(db: Session, id:int):
    try:
        query = db.query(Votacao).filter(Votacao.VotacaoID == id).first()
        return True if query else False
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def ja_votou(db: Session, votacao: Consulta_Votacao) -> bool:
    try:
        query = db.query(Voto).filter(Voto.VotacaoID == votacao.id_votacao,Voto.UtilizadorID == votacao.id_user).first()
        return query is not None
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

#Consulta as votações que ainda não foram processadas, contudo já se encontram expiradas
async def get_votacoes_expiradas_e_nao_processadas(db:Session):
    try:
        hoje = datetime.utcnow().date()
        ontem = hoje - timedelta(days=1)
        votacoes = db.query(Votacao).filter(Votacao.DataFim == ontem, Votacao.Processada == False).all()

        return votacoes
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

#Obtem todos os votos relativos a uma votação
async def get_votos_votacao(db:Session, votacao_id:int):
    try:
        votos = db.query(Voto).filter(Voto.VotacaoID == votacao_id).all()
        return votos
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

#Obtem o contexto da votação
async def get_contexto_votacao(db:Session, votacao_id:int):
    try:

        #Verificar se é uma votação de pedido novo recurso ou de manutenção
        if db.query(PedidoManutencao).filter(PedidoManutencao.PMID == votacao_id).first():
            return TipoVotacao.MANUTENCAO

        if db.query(VotacaoPedidoNovoRecurso.TipoVotacao).filter(VotacaoPedidoNovoRecurso.VotacaoID == votacao_id).first() == TipoVotacaoPedidoNovoRecurso.BINARIA.value:
            return TipoVotacaoPedidoNovoRecurso.BINARIA

        return TipoVotacaoPedidoNovoRecurso.MULTIPLA

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

#Obter orcamentos associados ao pedido de Manutenção
async def get_orcamentos_pm(db:Session, votacao_id:int):
    try:
        orcamentos = db.query(Orcamento).join(Orcamento.PedidoManutencao).filter(PedidoManutencao.VotacaoID==votacao_id).all()
        return orcamentos
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

#Obter os orcamentos associados a um pedido de novo recurso
async def get_orcamentos_pedido_novo_recurso_db(db:Session, votacao_id:int):
    try:
        orcamentos = (db.query(Orcamento)
                  .join(Orcamento.PedidoNovoRecurso)
                  .join(VotacaoPedidoNovoRecurso)
                  .filter(VotacaoPedidoNovoRecurso.VotacaoID==votacao_id).all())
        return orcamentos
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

#Obter todas as votações ativas, diferenciadas por tipos
async def listar_votacoes_ativas_db(db:Session):
    try:
        votacoes_pedido_recurso_binarias = (db.query(Votacao, VotacaoPedidoNovoRecurso.PedidoNovoRecID)
                                            .join(VotacaoPedidoNovoRecurso, VotacaoPedidoNovoRecurso.VotacaoID == Votacao.VotacaoID)
                                            .filter(Votacao.Processada != True, VotacaoPedidoNovoRecurso.TipoVotacao == TipoVotacaoPedidoNovoRecurso.BINARIA)
                                            .all())

        votacoes_pedido_recurso_mutliplas = (db.query(Votacao, VotacaoPedidoNovoRecurso.PedidoNovoRecID)
                                            .join(VotacaoPedidoNovoRecurso, VotacaoPedidoNovoRecurso.VotacaoID == Votacao.VotacaoID)
                                            .filter(Votacao.Processada != True, VotacaoPedidoNovoRecurso.TipoVotacao == TipoVotacaoPedidoNovoRecurso.MULTIPLA)
                                            .all())

        votacoes_pedido_manutencao = (db.query(Votacao, PedidoManutencao.PMID)
                                            .join(PedidoManutencao, PedidoManutencao.VotacaoID == Votacao.VotacaoID)
                                            .filter(Votacao.Processada != True)
                                            .all())

        return votacoes_pedido_recurso_binarias,votacoes_pedido_recurso_mutliplas,votacoes_pedido_manutencao
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

#Verificar se uma votação pertence a um pedido de manutencao
async def verificar_se_votacao_corresponde_a_pedido_manutencao_db(db:Session, votacao_id:int):
    try:
        val = db.query(PedidoManutencao).filter(PedidoManutencao.VotacaoID == votacao_id).first()

        if val:
            return True
        else: return False

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))