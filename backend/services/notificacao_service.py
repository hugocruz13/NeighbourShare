from sqlalchemy.orm import Session
from db.repository.notificacao_repo import *
from db.models import Notificacao, PedidoNovoRecurso
from fastapi import HTTPException
from schemas.notificacao_schema import *
from schemas.recurso_comum_schema import *
from schemas.orcamento_schema import *
from schemas.reserva_schema import *

#Cria uma notificação direcionada somente a um utilizador específico
async def cria_notificacao_individual_service(db:Session, notificacao:NotificacaoSchema, user_id:int):
    return await cria_notificacao_individual_db(db, notificacao, user_id)

#Cria uma notificação para todos os admins/gestores do sistema
async def cria_notificacao_admin_service(db:Session, notificacao:NotificacaoSchema):
    return await cria_notificacao_admin_db(db, notificacao)

#Cria uma notificação para todos os utilizadores
async def cria_notificacao_todos_service(db:Session, notificacao:NotificacaoSchema):
    return await cria_notificacao_todos_utilizadores_db(db,notificacao)

#Lista todas as notificações de um utilizador
async def listar_notificacoes_service(db:Session, user_id:int):

    lista_notificacoes = await notificacao_repo.listar_notificacoes_db(db, user_id)

    if not lista_notificacoes:
        raise HTTPException(status_code=400, detail="Nenhuma notificação encontrada")

    return lista_notificacoes

#region Votações
#TODO Criar notificação aquando da criação de uma votação

#TODO Cria notificação para o anuncio negativo do resultado de uma votação
#endregion

#region Manutenção de recurso comum

#Cria notificação referente à inserção de um novo pedido de manutenção de um recurso comum
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
            TipoProcessoID=await get_tipo_processo_id(db, TipoProcessoOpcoes.MANUTENCAO)
        )

        return await cria_notificacao_admin_db(db,notficacao)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Cria notificação a indicar a não necessidade de intervenção de uma entidade externa
async def cria_notificacao_nao_necessidade_entidade_externa(db:Session,pedido:PedidoManutencaoSchema):
    try:

        notificacao = NotificacaoSchema(
            Titulo= "Atualização sobre o seu pedido de manutenção",
            Mensagem= f"""
            
            Olá {pedido.Utilizador_.Nome},

            Agradecemos o seu pedido de manutenção referente a {pedido.DescPedido}.
            
            Informamos que, após análise, não será necessária a intervenção de uma entidade externa, uma vez que o problema poderá ser resolvido com os recursos internos do condomínio.
            
            A resolução será realizada brevemente, ou até pode já ter sido efetuada, por isso não se preocupe com a mesma.
            
            Agradecemos a sua colaboração e disponibilidade.
            """,
            ProcessoID= pedido.PMID,
            TipoProcessoID= await get_tipo_processo_id(db, TipoProcessoOpcoes.MANUTENCAO)
        )

        return await cria_notificacao_individual_db(db,notificacao,pedido.Utilizador_.UtilizadorID)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Cria notificação a indicar que orçamento foi o mais votado para a manutenção do recurso comum
async def cria_notificacao_orcamento_mais_votado(db:Session,pedido:PedidoManutencaoSchema, orcamento:OrcamentoSchema):
    try:

        notificacao = NotificacaoSchema(
            Titulo= "Orçamento aprovado para manutenção de recurso comum",
            Mensagem= f"""
                Prezados moradores,
                
                Informamos que, após o processo de avaliação e votação, foi escolhido o orçamento apresentado pela entidade {orcamento.Fornecedor} no valor de {orcamento.Valor}€ para a realização da manutenção do recurso comum {pedido.RecursoComun_.Nome}.
                
                A proposta selecionada foi a mais votada entre as opções apresentadas e cumpre os critérios estabelecidos.
                
                A entidade prestadora de serviços será informada e a manutenção será agendada brevemente. Informaremos aquando da conclusão da mesma.
                
                Agradeçemos a todos aqueles que expresseram o seu direito de voto
                """,
            ProcessoID= pedido.PMID,
            TipoProcessoID= await get_tipo_processo_id(db, TipoProcessoOpcoes.MANUTENCAO)
        )

        return await cria_notificacao_todos_utilizadores_db(db,notificacao)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Cria notificação a indicar a conclusão da manutenção do recurso comum
async def cria_notificacao_conclusao_manutencao_recurso_comum(db:Session,pedido:PedidoManutencaoSchema, orcamento:OrcamentoSchema):
    try:

        notificacao = NotificacaoSchema(
            Titulo= "Manutenção concluída com sucesso",
            Mensagem= f"""
                Prezados moradores,
    
                Vimos por este meio informar que a manutenção do recurso comum {pedido.RecursoComun_.Nome} foi concluída com sucesso.
                
                A intervenção foi realizada pela entidade {orcamento.Fornecedor}, conforme o orçamento previamente aprovado, garantindo o restabelecimento da normalidade no funcionamento do recurso.
                
                Agradecemos a compreensão e colaboração de todos durante este processo.
            """,
            ProcessoID= pedido.PMID,
            TipoProcessoID= await get_tipo_processo_id(db, TipoProcessoOpcoes.MANUTENCAO)
        )

        return await cria_notificacao_todos_utilizadores_db(db,notificacao)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#endregion

#region Aquisição novo recurso comum

#Cria um notificação referente à inserção de um novo pedido de aquisição de um recurso comum
async def cria_notificacao_insercao_pedido_novo_recurso_comum_service(db:Session,pedido:PedidoNovoRecursoSchema):
    try:
        notificacao = NotificacaoSchema(
            Titulo="Novo Pedido de Aquisição de Recurso Comum Submetido",
            Mensagem=f"""
                    O residente Nº:{pedido.Utilizador_.UtilizadorID} submeteu um novo pedido de aquisição de recurso comum.

                        ID do Pedido: {pedido.PedidoNovoRecID}
                        Data de Submissão: {pedido.DataPedido}

                    Solicita-se a análise e o início do processo de votação, conforme o fluxo definido para aprovação de novos recursos.

                    Pode aceder ao pedido diretamente através da plataforma para visualizar os detalhes e tomar as ações necessárias.
                    """,
            ProcessoID=pedido.PedidoNovoRecID,
            TipoProcessoID= await get_tipo_processo_id(db, TipoProcessoOpcoes.AQUISICAO)
        )

        return await cria_notificacao_admin_db(db,notificacao)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Cria notificação para o anuncio da compra que será efetuada para a aquisição do novo recurso comum
async def cria_notificacao_anuncio_compra_novo_recurso_comum_service(db: Session, pedido: PedidoNovoRecursoSchema, orcamento: OrcamentoSchema):
    try:
        notificao = NotificacaoSchema(
            Titulo="Confirmação da Aquisição de Novo Recurso",
            Mensagem=f"""

            Prezados moradores,

            Informamos que, após o processo de votação e análise dos orçamentos disponíveis, foi aprovada a aquisição do novo recurso
            referente ao pedido Nº {pedido.PedidoNovoRecID} com base no orçamento apresentado pela entidade {orcamento.Fornecedor}
            , no valor de {orcamento.Valor} €.

            Esta proposta foi a mais votada pelos moradores, cumprindo o critério de aprovação por maioria.

            Agradecemos a participação de todos no processo de decisão.

            """,
            ProcessoID=pedido.PedidoNovoRecID,
            TipoProcessoID=await get_tipo_processo_id(db, TipoProcessoOpcoes.AQUISICAO)
        )

        return await cria_notificacao_todos_utilizadores_db(db, notificao)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#endregion

#region Reserva de Recursos entre Vizinhos

#Cria notificação para notificar o recebimento de um novo pedido de reserva de um recurso
async def cria_notificacao_recebimento_pedido_reserva(db:Session, pedido:PedidoReservaSchema):
    try:
        notificacao = NotificacaoSchema(
            Titulo= "Novo pedido de reserva recebido",
            Mensagem= f"""
            Recebeu um novo pedido de reserva para o recurso {pedido.Recurso_.Nome}.

            Detalhes do pedido:
            
            Solicitado por: {pedido.Utilizador_.Nome}
            
            Período: {pedido.DataInicio} até {pedido.DataFim}
            
            Por favor, aceda aos seus pedidos de reserva para aceitar ou recusar o pedido.
            """,
            ProcessoID= pedido.PedidoResevaID,
            TipoProcessoID= await get_tipo_processo_id(db, TipoProcessoOpcoes.RESERVA)
        )

        return await cria_notificacao_individual_db(db,notificacao,pedido.Recurso_.UtilizadorID)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Cria notificação para notificar a recusa do pedido de reserva
async def cria_notificacao_recusa_pedido_reserva(db:Session, pedido:PedidoReservaSchema, motivo_recusa:str):
    try:
        notificacao = NotificacaoSchema(
            Titulo= "Pedido de reserva recusado",
            Mensagem=f"""
            O seu pedido nº {pedido.PedidoResevaID} para reservar o recurso {pedido.Recurso_.Nome} foi recusado.
            
            Motivo: {motivo_recusa}

            O dono lamenta o transtorno, contudo pode consultar os recursos disponíveis no sistema.
            """,
            ProcessoID=pedido.PedidoResevaID,
            TipoProcessoID= await get_tipo_processo_id(db, TipoProcessoOpcoes.RESERVA)
        )

        return await cria_notificacao_individual_db(db,notificacao,pedido.Utilizador_.UtilizadorID)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Cria notificação para notificar a aceitação do pedido de reserva
async def cria_notificacao_aceitacao_pedido_reserva(db:Session, pedido:PedidoReservaSchema):
    try:
        notificacao = NotificacaoSchema(
            Titulo= "Pedido de reserva aprovado",
            Mensagem= f"""
            O proprietário aceitou o seu pedido nº {pedido.PedidoResevaID} para reservar o recurso "{pedido.Recurso_.Nome}".
            
            Este mesmo pedido foi transformado em reserva, onde pode consultar a mesma na sua página de reservas.
            """,
            ProcessoID= pedido.PedidoResevaID,
            TipoProcessoID= await get_tipo_processo_id(db, TipoProcessoOpcoes.RESERVA)
        )

        return await cria_notificacao_individual_db(db,notificacao,pedido.Utilizador_.UtilizadorID)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Cria notificação para indicar que a caução será devolvida
async def cria_notificacao_caucao_devolucao_pedido_reserva(db:Session, pedido:PedidoReservaSchema, reserva_id:int):
    try:
        notificacao = NotificacaoSchema(
            Titulo= "Caução será devolvida",
            Mensagem= f"""
            
            A caução referente à reserva nº {reserva_id}, do recurso "{pedido.Recurso_.Nome}" será devolvida.
            
            O estado do recurso encontra-se aceitável, resultando assim na devolução futura da caução por parte do dono.
            
            Com isto, a reserva deste mesmo recurso dá-se por concluida.
            
            Caso tenha algum problema com a caução, contacte o seguinte numero de telemovel, referente ao dono do produto : {pedido.Recurso_.Utilizador_.Contacto}
            """,
            ProcessoID=pedido.PedidoResevaID,
            TipoProcessoID=await get_tipo_processo_id(db, TipoProcessoOpcoes.RESERVA)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Cria notificação a indicar que a caução não será devolvida
async def cria_notificacao_nao_caucao_devolucao_pedido_reserva(db:Session, pedido:PedidoReservaSchema, reserva_id:int, justificativa:str):
    try:
        notificacao = NotificacaoSchema(
            Titulo= "Caução não será devolvida",
            Mensagem= f"""
            A caução referente à reserva nº {reserva_id}, do recurso "{pedido.Recurso_.Nome}" não será devolvida.
            
            Motivo : {justificativa}
            
            Com isto, a reserva deste mesmo recurso dá-se por concluida.
            
            Contudo se sentir necessidade de entrar em contacto com o dono do produto, contacte o seguinte numero de telemovel : {pedido.Recurso_.Utilizador_.Contacto}
            """,
            ProcessoID= pedido.PedidoResevaID,
            TipoProcessoID= await get_tipo_processo_id(db, TipoProcessoOpcoes.RESERVA)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#endregion



