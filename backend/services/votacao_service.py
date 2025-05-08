from db.session import get_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.string_utils import formatar_string
from db.repository.votacao_repo import *
from db.repository.recurso_comum_repo import *
from datetime import date, datetime
from services.notificacao_service import *
from collections import defaultdict
from schemas.votacao_schema import *
from services.recurso_comum_service import *

scheduler = AsyncIOScheduler()

#criar votação
async def gerir_votacao_novo_recurso(db: Session, votacao: Criar_Votacao):
    try:
        #Formata as strings e remove espaços desnecessários
        votacao.titulo = formatar_string(votacao.titulo)
        votacao.descricao = formatar_string(votacao.descricao)

        #Verifica se o pedido existe
        val, id_estado_pedido = await existe_nr(db, votacao.id_processo)

        if not val:
            raise HTTPException(status_code=404, detail="Erro ao encontar pedido")

        #Verifica se a votação tem no mínimo 1 dia,
        if votacao.data_fim<= date.today():
            raise HTTPException(status_code=400, detail="A data de fim da votação deve ser posterior à data de início (mínimo 1 dia de duração).")

        tipovotacao = TipoVotacaoPedidoNovoRecurso.BINARIA

        if id_estado_pedido == EstadoPedNovoRecursoComumSchema.APROVADOPARAORCAMENTACAO.value:
            tipovotacao = TipoVotacaoPedidoNovoRecurso.MULTIPLA
            await cria_notificao_decisao_orcamento_novo_recurso_service(db, votacao)
        else:
            await cria_notificacao_decisao_novo_recurso_comum_service(db, votacao)
        await altera_estado_pedido_novo_recurso_db(db, votacao.id_processo,
                                                   EstadoPedNovoRecursoComumSchema.EMVOTACAO.value)
        return await criar_votacao_nr_db(db,votacao,tipovotacao)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def gerir_votacao_pedido_manutencao(db: Session, votacao: Criar_Votacao):
    try:
        #Formata as strings e remove espaços desnecessários
        votacao.titulo = formatar_string(votacao.titulo)
        votacao.descricao = formatar_string(votacao.descricao)

        #Verifica se o pedido de manutenção existe
        if not await existe_pedido_manutencao(db, votacao.id_processo):
            raise HTTPException(status_code=404, detail="Erro ao encontar manutenção")

        #Verifica se a votação tem no mínimo 1 dia,
        if votacao.data_fim <= date.today():
            raise HTTPException(status_code=400, detail="A data de fim da votação deve ser posterior à data de início (mínimo 1 dia de duração).")

        await cria_notificacao_decisao_orcamento_manutencao_service(db, votacao)

        return await criar_votacao_pedido_manutencao_db(db,votacao)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#votar
async def gerir_voto(db: Session, voto:Votar_id):
    try:
        #Formata as strings e remove espaços desnecessários
        voto.voto = formatar_string(voto.voto)

        #Verifica se a votação existe
        if not await existe_votacao(db, voto.id_votacao):
            raise HTTPException(status_code=404, detail="Erro ao encontar votação")

        if ja_votou(db, Consulta_Votacao(id_votacao=voto.id_votacao, id_user=voto.id_user)):
            raise HTTPException(status_code=403, detail="Utilizador já registou a votação")

        return await registar_voto(db,voto)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Verifica as votações que tem como data de término o dia anterior ao atual e calcula os resultados
async def processar_votacoes_expiradas(db:Session):
    try:
        resultado = ""

        votacoes_expiradas = await get_votacoes_expiradas_e_nao_processadas(db)

        for votacao in votacoes_expiradas:
            votos = await get_votos_votacao(db, votacao.id_votacao)

            contagem = defaultdict(int)

            for voto in votos:
                if voto.EscolhaVoto:
                    contagem[voto.EscolhaVoto] += 1

            if contagem:
                resultado = max(contagem.items(), key=lambda item: item[1])[0]
            else:
                resultado = "Sem votos"

            votacao.Processada = True

            tipo_votacao  = await get_contexto_votacao(db, votacao.id_votacao)

            if tipo_votacao == TipoVotacao.MANUTENCAO and resultado != "Sem votos":
                await cria_notificacao_orcamento_mais_votado(db,await obter_pedido_manutencao_db(db,votacao.id_processo),resultado)
                await criar_manutencao_service(db, ManutencaoCreateSchema(
                    PMID=votacao.PedidoManutencao[0].PMID,
                    DataManutencao=datetime.datetime.min,
                    DescManutencao=votacao.PedidoManutencao[0].DescPedido,
                    Orcamento_id=int(resultado)))
            elif tipo_votacao == TipoVotacaoPedidoNovoRecurso.MULTIPLA and resultado != "Sem votos":
                await altera_estado_pedido_novo_recurso_db(db,votacao.id_processo,EstadoPedNovoRecursoComumSchema.APROVADOPARACOMPRA.value)
                await cria_notificacao_anuncio_compra_novo_recurso_comum_service(db,await obter_pedido_novo_recurso_db(db,votacao.id_processo),resultado)
            elif tipo_votacao == TipoVotacaoPedidoNovoRecurso.BINARIA and resultado == formatar_string("Sim"):
                await altera_estado_pedido_novo_recurso_db(db, votacao.id_processo,EstadoPedNovoRecursoComumSchema.APROVADOPARAORCAMENTACAO.value)
                await cria_notificacao_decisao_compra_recurso_positiva_service(db,votacao,await obter_pedido_novo_recurso_db(db,votacao.id_processo))
            elif tipo_votacao == TipoVotacaoPedidoNovoRecurso.BINARIA and resultado == formatar_string("Não"):
                await altera_estado_pedido_novo_recurso_db(db, votacao.id_processo, EstadoPedNovoRecursoComumSchema.REJEITADO.value)
                await cria_notificacao_decisao_nao_compra_recurso_service(db, votacao,await obter_pedido_novo_recurso_db(db,votacao.id_processo))

        db.commit()

        return True
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Função para testar o processamento de uma votação e obtenção dos resultados
async def processar_votacao(db:Session, votacao_id: int):
    try:
        if not await existe_votacao(db, votacao_id):
            raise HTTPException(status_code=404, detail="Votação não existe!")

        votos = await get_votos_votacao(db, votacao_id)

        contagem = defaultdict(int)

        for voto in votos:
            if voto.EscolhaVoto:
                contagem[voto.EscolhaVoto] += 1

        votacao = db.query(Votacao).filter(Votacao.VotacaoID == votacao_id).first()

        if contagem:
            resultado = max(contagem.items(), key=lambda item: item[1])[0]

            if await verificar_se_votacao_corresponde_a_pedido_manutencao_db(db, votacao_id):
                await criar_manutencao_service(db, ManutencaoCreateSchema(
                    PMID=votacao.PedidoManutencao[0].PMID,
                    DataManutencao= datetime.datetime.min,
                    DescManutencao=votacao.PedidoManutencao[0].DescPedido,
                    Orcamento_id= int(resultado)
                ))
                await alterar_tipo_estado_pedido_manutencao(db,votacao.PedidoManutencao[0].PMID, EstadoPedManutencaoSchema.NEGOCIACAOENTIDADESEXTERNAS.value)
                await cria_notificacao_orcamento_mais_votado(db,await obter_pedido_manutencao_db(db, votacao.PedidoManutencao[0].PMID),resultado)
            else:

                votacao_pedido_novo_recurso = db.query(VotacaoPedidoNovoRecurso).filter(VotacaoPedidoNovoRecurso.VotacaoID == votacao_id).first()

                if votacao_pedido_novo_recurso.TipoVotacao == TipoVotacaoPedidoNovoRecurso.MULTIPLA and resultado != "Sem votos":
                    await altera_estado_pedido_novo_recurso_db(db,votacao_pedido_novo_recurso.PedidoNovoRecID,EstadoPedNovoRecursoComumSchema.APROVADOPARACOMPRA.value)
                    await cria_notificacao_anuncio_compra_novo_recurso_comum_service(db,await obter_pedido_novo_recurso_db(db,votacao_pedido_novo_recurso.PedidoNovoRecID),resultado)
                elif votacao_pedido_novo_recurso.TipoVotacao == TipoVotacaoPedidoNovoRecurso.BINARIA and resultado == "sim":
                    await altera_estado_pedido_novo_recurso_db(db, votacao_pedido_novo_recurso.PedidoNovoRecID,EstadoPedNovoRecursoComumSchema.APROVADOPARAORCAMENTACAO.value)
                    await cria_notificacao_decisao_compra_recurso_positiva_service(db,votacao,await obter_pedido_novo_recurso_db(db,votacao_pedido_novo_recurso.PedidoNovoRecID))
                elif votacao_pedido_novo_recurso.TipoVotacao == TipoVotacaoPedidoNovoRecurso.BINARIA and resultado == "nao":
                    await altera_estado_pedido_novo_recurso_db(db, votacao_pedido_novo_recurso.PedidoNovoRecID, EstadoPedNovoRecursoComumSchema.REJEITADO.value)
                    await cria_notificacao_decisao_nao_compra_recurso_service(db, votacao,await obter_pedido_novo_recurso_db(db,votacao_pedido_novo_recurso.PedidoNovoRecID))

        else:
            resultado = "Sem votos"

        votacao.Processada = True

        db.commit()

        return {'Votação processada, resultado: ' + resultado}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def check_votacoes_expiradas():
    db: Session = next(get_db())
    try:
        processar_votacoes_expiradas(db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def gerir_votacoes_orcamentos_pm(db:Session, votacao_id: int):
    try:
        if not await existe_votacao(db, votacao_id):
            raise HTTPException(status_code=404, detail="Votação não encontrado")

        return await get_orcamentos_pm(db, votacao_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Obter todos os orçamentos registados associados a um pedido de aquisição de um novo recurso
async def get_orcamentos_pedido_novo_recurso_service(db:Session, votacao_id: int):
    try:
        if not await existe_votacao(db, votacao_id):
            raise HTTPException(status_code=404, detail="Votação não encontrado")

        return await get_orcamentos_pedido_novo_recurso_db(db,votacao_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def listar_votacoes_ativas(db:Session):
    try:
        votacoes_pedido_recurso_binarias, votacoes_pedido_recurso_mutliplas, votacoes_pedido_manutencao = await listar_votacoes_ativas_db(db)

        lista_votacoes_pr_binarias = []
        lista_votacoes_pr_multiplas = []
        lista_votacoes_pm = []

        for votacao, pedido_id in votacoes_pedido_recurso_binarias:
            new_votacao = VotacaoGet(
                votacao_id=votacao.VotacaoID,
                titulo=votacao.Titulo,
                descricao=votacao.Descricao,
                data_inicio = votacao.DataInicio,
                data_fim = votacao.DataFim,
                pedido_recurso = pedido_id
            )
            lista_votacoes_pr_binarias.append(new_votacao)
        for votacao, pedido_id in votacoes_pedido_recurso_mutliplas:
            new_votacao = VotacaoGet(
                votacao_id=votacao.VotacaoID,
                titulo=votacao.Titulo,
                descricao=votacao.Descricao,
                data_inicio = votacao.DataInicio,
                data_fim = votacao.DataFim,
                pedido_recurso = pedido_id
            )
            lista_votacoes_pr_multiplas.append(new_votacao)
        for votacao, pedido_id in votacoes_pedido_manutencao:
            new_votacao = VotacaoGet(
                votacao_id=votacao.VotacaoID,
                titulo=votacao.Titulo,
                descricao=votacao.Descricao,
                data_inicio=votacao.DataInicio,
                data_fim=votacao.DataFim,
                pedido_recurso=pedido_id
            )
            lista_votacoes_pm.append(new_votacao)

        return ObtemTodasVotacoes(
            lista_votacao_pedido_novo_recurso_binarias = lista_votacoes_pr_binarias,
            lista_votacao_pedido_novo_recurso_multiplas = lista_votacoes_pr_multiplas,
            lista_votacao_pedido_manutencao = lista_votacoes_pm
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))