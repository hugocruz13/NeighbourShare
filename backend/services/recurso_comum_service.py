import services.notificacao_service as notificacao_service
import os
from requests import Session
import db.repository.recurso_comum_repo as recurso_comum_repo
import db.session as session
from fastapi import HTTPException, UploadFile
from schemas.notificacao_schema import *
from db.repository.notificacao_repo import get_tipo_processo_id
from datetime import date
from db.models import Notificacao, PedidoManutencao
from schemas.recurso_comum_schema import *
from services.notificacao_service import *
from schemas.recurso_comum_schema import *
from schemas.user_schemas import UserJWT
from db.repository.orcamento_repo import get_orcamento_by_id

#region Gestão dos Recursos Comuns

#Inserir um novo recurso comum
async def inserir_recurso_comum_service(db:session, recurso_comum:RecursoComumSchemaCreate, imagem:UploadFile):
    try:
        recurso = await recurso_comum_repo.inserir_recurso_comum_db(db, recurso_comum)
        path = await guardar_imagem(imagem, recurso.RecComumID)
        if await recurso_comum_repo.update_imagem(db, path, recurso.RecComumID):
            return RecursoComum_Return(id=recurso.RecComumID, nome=recurso.Nome, desc=recurso.DescRecursoComum, path=path)
        else:
            raise RuntimeError("Erro ao guardar imagem do recurso comum")
    except Exception as e:
        return False, {"details": str(e)}

async def guardar_imagem(imagem:UploadFile, id:int):
    try:
        tipos_permitidos = ['image/png', 'image/jpeg', 'image/jpg']

        if imagem.content_type not in tipos_permitidos:
            raise HTTPException (status_code=400, detail="Apenas imagens são permitidas (png, jpeg, jpg)")

        pasta_imagens = os.getenv('UPLOAD_DIR_RECURSOCOMUM')

        imagem_path = os.path.join(pasta_imagens, str(id)).replace("\\", "/")


        os.makedirs(imagem_path, exist_ok=True)

        caminho_arquivo = os.path.join(imagem_path, imagem.filename).replace("\\", "/")

        with open(caminho_arquivo,'wb+') as f:
            f.write(imagem.file.read())

        url_imagens = os.getenv('SAVE_RECURSOCOMUM')
        path = os.path.join(url_imagens,str(id), imagem.filename)
        clean_path = path.replace("\\", "/")
        return clean_path

    except Exception as e:
        return False, {"details": str(e)}

#Substitui uma imagem de um recurso comum
async def substitui_imagem_recurso_comum_service(id_recurso_comum: int, imagem:Optional[UploadFile]):
    try:

        if imagem is None:
            return False
        elif imagem.content_type not in ['image/png', 'image/jpeg', 'image/jpg']:
            raise HTTPException (status_code=400, detail="Apenas imagens são permitidas (png, jpeg, jpg)")

        caminho_pasta_recurso = os.path.join(os.getenv('UPLOAD_DIR_RECURSOCOMUM'),str(id_recurso_comum)).replace("\\", "/")
        caminho_nova_imagem = os.path.join(os.getenv('UPLOAD_DIR_RECURSOCOMUM'),str(id_recurso_comum), imagem.filename).replace("\\", "/")

        for nome_arquivo in os.listdir(caminho_pasta_recurso):
            caminho_arquivo = os.path.join(caminho_pasta_recurso, nome_arquivo).replace("\\", "/")
            if os.path.isfile(caminho_arquivo):
                if nome_arquivo != imagem.filename:
                    os.remove(caminho_arquivo)
                elif nome_arquivo == imagem.filename:
                    return False

        return await guardar_imagem(imagem, id_recurso_comum)

    except Exception as e:
        raise e

#Faz a atualização dos dados de um recurso comum
async def update_recurso_comum_service(recurso_comum_id: int, recurso_comum_update: RecursoComunUpdate, db:session):
    try:
        return await recurso_comum_repo.update_recurso_comum_db(recurso_comum_id,recurso_comum_update,db)
    except Exception as e:
        raise e

#Elimina um recurso comum
async def eliminar_recurso_comum_service(recurso_comum_id: int, db:session):
    try:
        if await verificar_possibilidade_eliminar_recurso_comum_service(recurso_comum_id, db):
            return await recurso_comum_repo.eliminar_recurso_comum_db(recurso_comum_id,db)
        else: return {'Recurso comum numa pedido de manutenção ativo'}
    except Exception as e:
        raise e

#Verifica se um recurso comum pode ser eliminado
async def verificar_possibilidade_eliminar_recurso_comum_service(recurso_comum_id: int, db:session):
    try:
        if await recurso_comum_repo.verifica_eliminar_recurso_comum_db(recurso_comum_id, db):
            return True
        else: return False
    except Exception as e:
        raise e

async def get_recursos_comuns(db:session):
    try:
        return await recurso_comum_repo.obter_recrusos_comuns(db)
    except Exception as e:
        return False, {"details": str(e)}

async def get_recursos_comuns_by_id(db:session, id:int):
    try:
        return await recurso_comum_repo.obter_recrusos_comuns_by_id(db, id)
    except Exception as e:
        return False, {"details": str(e)}

#endregion

#region Pedidos de Novos Recursos Comuns

#Inserir um pedido de um novo recurso comum
async def inserir_pedido_novo_recurso_service(db:session, pedido:PedidoNovoRecursoSchemaCreate):
    try:
        msg,novo_pedido = await recurso_comum_repo.inserir_pedido_novo_recurso_db(db,pedido)

        msg_noti = await notificacao_service.cria_notificacao_insercao_pedido_novo_recurso_comum_service(db, novo_pedido) #Criação da notificação

        return msg,msg_noti
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def listar_pedidos_novos_recursos_service(db:session):
    pedidos_novos_recursos = await recurso_comum_repo.listar_pedidos_novos_recursos_db(db)

    if not pedidos_novos_recursos:
        raise HTTPException(status_code=400, detail="Nenhum pedido de novo recurso encontrado")

    return pedidos_novos_recursos

#endregion

#region Pedidos de Manutenção

#Inserir um pedido de manutenção de um recurso comum
async def inserir_pedido_manutencao_service(db:session, pedido:PedidoManutencaoSchemaCreate):
    try:

        msg, novo_pedido = await recurso_comum_repo.inserir_pedido_manutencao_db(db,pedido)

        msg_noti = await notificacao_service.cria_notificacao_insercao_pedido_manutencao_service(db, novo_pedido) #Criação da notificação

        return msg, msg_noti

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Listar pedidos de manutenção
async def listar_pedidos_manutencao_service(db:session):

    pedidos_manutencao = await recurso_comum_repo.listar_pedidos_manutencao_db(db)

    if not pedidos_manutencao:
        raise HTTPException(status_code=400, detail="Nenhum pedido de manutenção encontrado")

    return pedidos_manutencao

async def obter_all_tipo_estado_pedido_manutencao(db:session):
    try:
        return await recurso_comum_repo.obter_all_tipo_estado_pedido_manutencao(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def alterar_tipo_estado_pedido_manutencao(db:session, id_pedido_manutencao:int, tipo_estado_pedido_manutencao:int):
    try:
        estados = await obter_all_tipo_estado_pedido_manutencao(db)
        if estados is None:
            raise HTTPException(status_code=500, detail="Erro ao obter tipos de estado de pedido manutenção")
        for e in estados:
            print(e.EstadoPedManuID)
            print(tipo_estado_pedido_manutencao)
            if e.EstadoPedManuID == int(tipo_estado_pedido_manutencao):
                await recurso_comum_repo.alterar_estado_pedido_manutencao(db, id_pedido_manutencao, tipo_estado_pedido_manutencao)
                if e.EstadoPedManuID == 2:  # Estado -> Aprovado para manutenção interna
                    await notificacao_service.cria_notificacao_nao_necessidade_entidade_externa(db,await obter_pedido_manutencao(db,id_pedido_manutencao))
                elif e.EstadoPedManuID == 3: # Estado -> Em negociação com entidades externas
                    await notificacao_service.cria_notificacao_necessidade_entidade_externa(db,await obter_pedido_manutencao(db,id_pedido_manutencao))
                elif e.EstadoPedManuID == 4: # Estado -> Rejeitado
                    await notificacao_service.cria_notificacao_rejeicao_manutencao_recurso_comum(db,await obter_pedido_manutencao(db,id_pedido_manutencao))
                return True
        return False
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def obter_pedido_manutencao(db:Session, id_manutencao:int):
    try:
        return await recurso_comum_repo.obter_pedido_manutencao_db(db, id_manutencao)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_pedido_manutencao(db:Session, u_pedido:PedidoManutencaoUpdateSchema, token:UserJWT):
    try:
        pedido_manutencao = await obter_pedido_manutencao(db, u_pedido.PMID)
        if u_pedido.DescPedido is None:
            return False, "Descrição do Pedido não introduzida"
        elif  pedido_manutencao.UtilizadorID != token.id:
            return False, "Utilizador não têm permissão para alterar os dados do pedido de manutenção"
        return True, await recurso_comum_repo.update_pedido_manutencao_db(db, u_pedido)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Elimina um pedido de manutenção
async def eliminar_pedido_manutencao_service(db:Session, pedido_id:int, token:UserJWT):
    try:
        pedido_manutencao = await obter_pedido_manutencao(db, pedido_id)
        if token.role == "residente" and pedido_manutencao.UtilizadorID != token.id:
            return {'Utilizador não têm permissão para alterar os dados do pedido de manutenção'}
        return await recurso_comum_repo.eliminar_pedido_manutencao(db, pedido_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#endregion

#region Manutenção de Recursos Comuns

async def criar_manutencao_service(db:session, manutencao:ManutencaoCreateSchema):
    try:
        #verifica se o pedido existe
        if not await recurso_comum_repo.obter_pedido_manutencao_db(db, manutencao.PMID):
            raise HTTPException(status_code=400, detail="Pedido de manutenção não existe")

        #verifica se o orcamento existe
        if not await get_orcamento_by_id(db, manutencao.Orcamento_id):
            raise HTTPException(status_code=400, detail="Orçamento não existe")

        return await recurso_comum_repo.criar_manutencao_db(db,manutencao)
    except Exception as e:
        raise e

async def visualizar_manutencoes(db:session):
    manutencoes = await recurso_comum_repo.listar_manutencoes_db(db)

    if not manutencoes:
        raise HTTPException(status_code=400, detail="Nenhuma manutenção encontrada")
    return manutencoes

async def obter_all_tipo_estado_manutencao(db:session):
    try:
        return await recurso_comum_repo.obter_all_tipo_estado_manutencao(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def alterar_tipo_estado_manutencao(db:session, id_manutencao:int, tipo_estado_manutencao:int):
    try:
        estados = await obter_all_tipo_estado_manutencao(db)
        if estados is None:
            raise HTTPException(status_code=500, detail="Erro ao obter tipos de estado manutenção")
        if tipo_estado_manutencao in [estado.EstadoManuID for estado in estados]:
            await recurso_comum_repo.alterar_estado_manutencao(db, id_manutencao, tipo_estado_manutencao)
            return True
        else:
            return False
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def obter_manutencao(db:Session, id_manutencao:int):
    try:
        manutencao = await recurso_comum_repo.obter_manutencao_db(db, id_manutencao)
        if manutencao is None:
            raise HTTPException(status_code=500, detail=str("Manutenção não encontrada"))
        return manutencao
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_manutencao(db:Session, u_pedido:ManutencaoUpdateSchema):
    try:
        if u_pedido.ManutencaoID is None or u_pedido.PMID is None or u_pedido.DataManutencao is None or u_pedido.DescManutencao is None:
            raise HTTPException(status_code=400, detail="Erro, um dos campos não foi preenchido")
        a = await recurso_comum_repo.update_manutencao_db(db, u_pedido)
        if a is None:
            raise HTTPException(status_code=400, detail="Erro, a atualizar manutenção")
        return a
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def eliminar_manutencao_service(db:Session, id_manutencao:int):
    try:
        return await recurso_comum_repo.eliminar_manutencao_db(db, id_manutencao)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#endregion

