from sqlalchemy.orm import Session
from db.repository.notificacao_repo import *
from db.models import Notificacao, PedidoNovoRecurso
from fastapi import HTTPException
from schemas.notificacao_schema import *
from schemas.recurso_comum_schema import *

async def cria_notificacao_individual_service(db:Session, notificacao:Notificacao, user_id:int):
    return await cria_notificacao_individual_db(db, notificacao, user_id)

async def cria_notificacao_admin_service(db:Session, notificacao:NotificacaoSchema):
    return await cria_notificacao_admin_db(db, notificacao)

async def cria_notificacao_todos_service(db:Session, notificacao:Notificacao):
    return await cria_notificacao_todos_utilizadores_db(db,notificacao)

async def listar_notificacoes_service(db:Session, user_id:int):

    lista_notificacoes = listar_notificacoes_db(db, user_id)

    if not lista_notificacoes:
        raise HTTPException(status_code=400, detail="Nenhuma notificação encontrada")

    return lista_notificacoes

async def cria_notificacao_insercao_pedido_novo_recurso_comum_service(db:Session,pedido:PedidoNovoRecursoSchema):
    try:
        notificacao = NotificacaoSchema(
            Titulo="Novo Pedido de Aquisição de Recurso Comum Submetido",
            Mensagem=f"""
                    O residente Nº:{pedido.Utilizador_.UtilizadorID} submeteu um novo pedido de aquisição de recurso comum.

                        ID do Pedido: {pedido.PedidoNovoRecursoID}
                        Data de Submissão: {pedido.DataHora}

                    Solicita-se a análise e o início do processo de votação, conforme o fluxo definido para aprovação de novos recursos.

                    Pode aceder ao pedido diretamente através da plataforma para visualizar os detalhes e tomar as ações necessárias.
                    """,
            ProcessoID=pedido.PedidoNovoRecursoID,
            TipoProcessoID=get_tipo_processo_id(db, TipoProcessoOpcoes.AQUISICAO)
        )

        return await cria_notificacao_admin_db(db,notificacao)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def cria_notificacao_insercao_pedido_manutencao_service(db:Session,pedido:PedidoManutencaoSchema):
    try:
        notficacao = NotificacaoSchema(
            Titulo="Novo Pedido de Manutenção de Recurso Comum Submetido",
            Mensagem=f"""
                            O residente Nº:{pedido.Utilizador_.UtilizadorID} submeteu um novo pedido de manutenção do recurso comum com o Nº:{pedido.RecursoComun_.RecComumID}.

                                ID do Pedido: {pedido.PMID}
                                Data de Submissão: {pedido.DataPedido}

                            Solicita-se a análise e o início do processo de votação, conforme o fluxo definido para aprovação de novos recursos.

                            Pode aceder ao pedido diretamente através da plataforma para visualizar os detalhes e tomar as ações necessárias.
                            """,
            ProcessoID=pedido.PMID,
            TipoProcessoID=get_tipo_processo_id(db, TipoProcessoOpcoes.MANUTENCAO)
        )

        return await cria_notificacao_admin_db(db,notficacao)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
