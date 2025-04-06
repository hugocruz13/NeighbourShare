import db.repository.recurso_repo as recurso_repo
import db.session as session
from fastapi import HTTPException, UploadFile
import os

async def get_disponibilidade_id_service(db:session, disponibilidade:str):

    disponibilidade_id = recurso_repo.get_disponibilidade_id_db(db, disponibilidade)

    return disponibilidade_id

async def inserir_recurso_service(db:session, novo_recurso, imagem_recurso:UploadFile):
    try:
        recurso_id, mensagem = await recurso_repo.inserir_recurso_db(db, novo_recurso)
        if recurso_id :
            return await guardar_imagem_recurso(imagem_recurso, recurso_id)
        else:
            return False, "Erro ao guardar a imagem referente ao recurso"
    except Exception as e:
        return False, "details: "+str(e)

async def guardar_imagem_recurso(imagem_recurso:UploadFile, recurso_id:int):
    try:

        tipos_permitidos = ['image/png', 'image/jpeg', 'image/jpg']

        if imagem_recurso.content_type not in tipos_permitidos:
            raise HTTPException (status_code=400, detail="Apenas imagens são permitidas (png, jpeg, jpg)")

        pasta_imagens = os.getenv('UPLOAD_DIR_RECURSO')

        imagem_path = os.path.join(pasta_imagens, str(recurso_id))

        os.makedirs(imagem_path, exist_ok=True)

        caminho_arquivo = os.path.join(imagem_path, imagem_recurso.filename)

        with open(caminho_arquivo,'wb+') as f:
            f.write(imagem_recurso.file.read())

        return True, {"Imagem guardada com sucesso"}

    except Exception as e:
        return False, {"details: "+ str(e)}

async def lista_recursos_service(db:session):

    lista_recursos = await recurso_repo.listar_recursos_db(db)

    if not lista_recursos:
        raise HTTPException(status_code=400, detail="Nenhum recurso encontrado")

    return lista_recursos

async def lista_recursos_disponiveis_service(db:session):

    lista_recursos_disponiveis = await recurso_repo.listar_recursos_disponiveis_db(db)

    if not lista_recursos_disponiveis:
        raise HTTPException(status_code=400, detail="Nenhum recurso disponivel encontrado")

    return lista_recursos_disponiveis

async def lista_recursos_indisponiveis_service(db:session):

    lista_recursos_indisponiveis = await recurso_repo.listar_recursos_indisponiveis(db)

    if not lista_recursos_indisponiveis:
        raise HTTPException(status_code=400, detail="Nenhum recurso indisponivel encontrado")

    return lista_recursos_indisponiveis