from db.session import get_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.string_utils import formatar_string
from db.repository.votacao_repo import *
from db.repository.recurso_comum_repo import *
from datetime import date
from services.notificacao_service import *
from collections import defaultdict

scheduler = AsyncIOScheduler()

#criar votação
async def gerir_votacao_novo_recurso(db: Session, votacao: Criar_Votacao):
    try:
        #Formata as strings e remove espaços desnecessários
        votacao.titulo = formatar_string(votacao.titulo)
        votacao.descricao = formatar_string(votacao.descricao)

        #Verifica se o pedido existe
        val, desc_estado_pedido = await existe_nr(db, votacao.id_processo)

        if not val:
            raise HTTPException(status_code=404, detail="Erro ao encontar pedido")

        #Verifica se a votação tem no mínimo 1 dia,
        if votacao.data_fim<= date.today():
            raise HTTPException(status_code=400, detail="A data de fim da votação deve ser posterior à data de início (mínimo 1 dia de duração).")

        tipovotacao = TipoVotacaoPedidoNovoRecurso.BINARIA

        if desc_estado_pedido == EstadoPedNovoRecursoComumSchema.APROVADOPARAORCAMENTACAO.value:
            tipovotacao = TipoVotacaoPedidoNovoRecurso.MULTIPLA
            await cria_notificao_decisao_orcamento_novo_recurso_service(db, votacao)
        else:
            await cria_notificacao_decisao_novo_recurso_comum_service(db, votacao)

        return await criar_votacao_nr_db(db,votacao,tipovotacao)
    except Exception as e:
        raise e

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
    except Exception as e:
        raise e

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
    except Exception as e:
        raise e

#Verifica as votações que tem como data de término o dia anterior ao atual e calcula os resultados
async def processar_votacoes_expiradas(db:Session):

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
        elif tipo_votacao == TipoVotacaoPedidoNovoRecurso.MULTIPLA and resultado != "Sem votos":
            await cria_notificacao_anuncio_compra_novo_recurso_comum_service(db,await obter_pedido_novo_recurso_db(db,votacao.id_processo),resultado)
        elif tipo_votacao == TipoVotacaoPedidoNovoRecurso.BINARIA and resultado == formatar_string("Sim"):
            await cria_notificacao_decisao_compra_recurso_positiva_service(db,votacao,await obter_pedido_novo_recurso_db(db,votacao.id_processo))
        elif tipo_votacao == TipoVotacaoPedidoNovoRecurso.BINARIA and resultado == formatar_string("Não"):
            await cria_notificacao_decisao_nao_compra_recurso_service(db, votacao,await obter_pedido_novo_recurso_db(db,votacao.id_processo))

    db.commit()

    return True

#Função para testar o processamento de uma votação e obtenção dos resultados
async def processar_votacao(db:Session, votacao_id: int):
    try:
        votos = await get_votos_votacao(db, votacao_id)

        contagem = defaultdict(int)

        for voto in votos:
            if voto.EscolhaVoto:
                contagem[voto.EscolhaVoto] += 1

        if contagem:
            resultado = max(contagem.items(), key=lambda item: item[1])[0]
        else:
            resultado = "Sem votos"

        votacao = db.query(Votacao).filter(Votacao.VotacaoID == votacao_id).first()

        votacao.Processada = True

        db.commit()

        return {'Votação processada, resultado: ' + resultado}

    except HTTPException as he:
        raise he

def check_votacoes_expiradas():
    db: Session = next(get_db())
    try:
        processar_votacoes_expiradas(db)
    finally:
        db.close()

async def gerir_votacoes_orcamentos_pm(db:Session, votacao_id: int):
    try:
        if not await existe_votacao(db, votacao_id):
            raise HTTPException(status_code=404, detail="Votação não encontrado")

        return await get_orcamentos_pm(db, votacao_id)
    except Exception as e:
        raise e