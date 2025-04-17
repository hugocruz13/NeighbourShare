from dotenv import load_dotenv
from pathlib import Path
import db.repository.recurso_repo as recurso_repo
import db.session as session
from fastapi import HTTPException, UploadFile
from schemas.recurso_schema import *
import os
import dotenv
from tempfile import SpooledTemporaryFile

async def get_disponibilidade_id_service(db:session, disponibilidade:str):

    disponibilidade_id = recurso_repo.get_disponibilidade_id_db(disponibilidade,db)

    return disponibilidade_id

async def get_categoria_id_service(db:session, categoria:str):
    categoria_id = recurso_repo.get_categoria_id_db(categoria,db)

    return categoria_id

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

        return True, {"message": "Imagem guardada com sucesso"}
    except Exception as e:
        return False, {"details": str(e)}

#Lista todos os recursos existentes no sistema
async def lista_recursos_service(db:session):

    lista_recursos = await recurso_repo.listar_recursos_db(db)

    if not lista_recursos:
        raise HTTPException(status_code=400, detail="Nenhum recurso encontrado")

    lista_recursos_imagens = await lista_imagens_recursos_service(lista_recursos)

    if not lista_recursos_imagens:
        raise HTTPException(status_code=400, detail="Erro no carregameto das imagens dos recursos")

    return lista_recursos_imagens

#Lista as informações relativas a um recurso registado no sistema
async def lista_recurso_service(db:session, recurso_id:int):

    recurso = await recurso_repo.listar_recurso_db(db, recurso_id)

    if not recurso:
        raise HTTPException(status_code=400, detail="Nenhum recurso encontrado")

    image_path = await carrega_imagem_recurso_service(recurso_id)

    recurso.Image = image_path

    return recurso

#Lista os recursos de um utilizador
async def lista_recursos_utilizador_service(db:session, utilizador_id:int):

    lista_recursos = await recurso_repo.listar_recursos_utilizador_db(db, utilizador_id)

    if not lista_recursos:
        raise HTTPException(status_code=400, detail="Nenhum recurso encontrado")

    lista_recursos_utilizador = []

    for recurso in lista_recursos:

        recurso_utilizador = RecursoGetUtilizadorSchema(
            RecursoID= recurso.RecursoID,
            Nome=recurso.Nome,
            Caucao=recurso.Caucao,
            Categoria_=recurso.Categoria_,
            Disponibilidade_=recurso.Disponibilidade_,
        )

        lista_recursos_utilizador.append(recurso_utilizador)

    return lista_recursos_utilizador

#Obtem as imagens referentes a uma lista de recursos
async def lista_imagens_recursos_service(lista_recursos:list):

    lista_recursos_imagens = []

    for recurso in lista_recursos:

        caminho_foto_recurso = await carrega_imagem_recurso_service(recurso.RecursoID)

        if not caminho_foto_recurso:
            caminho_foto_recurso = None

        novo_recurso = RecursoGetTodosSchema(
            RecursoID = recurso.RecursoID,
            Nome = recurso.Nome,
            DescRecurso = recurso.DescRecurso,
            Caucao = recurso.Caucao,
            Categoria_ = recurso.Categoria_,
            Disponibilidade_ = recurso.Disponibilidade_,
            Image = caminho_foto_recurso
        )

        lista_recursos_imagens.append(novo_recurso)

    return lista_recursos_imagens

async def carrega_imagem_recurso_service(recurso_id:int):

    load_dotenv()

    pasta_path = os.path.join(os.getenv('UPLOAD_DIR_RECURSO'), str(recurso_id))

<<<<<<< HEAD
    if not os.path.exists(pasta_path):
        os.makedirs(pasta_path)

=======
>>>>>>> origin/votação
    pasta = Path(pasta_path)

    arquivos = [f for f in pasta.iterdir() if f.is_file()]

    if not arquivos:
<<<<<<< HEAD
        return None
=======
        raise FileNotFoundError("Nenhuma foto encontrada")
>>>>>>> origin/votação

    imagem_path = str(arquivos[0])

    return imagem_path

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