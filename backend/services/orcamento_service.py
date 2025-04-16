import os
from dotenv import load_dotenv
import db.repository.orcamento_repo as orcamento_repo
import schemas.orcamento_schema as orcamentoschema
import db.session as session
from fastapi import UploadFile
from schemas.orcamento_schema import OrcamentoUpdateSchema, OrcamentoGetSchema
import shutil
from pathlib import Path


#Service para inserir um novo orçamento
async def inserir_orcamento_service(db:session, orcamento:orcamentoschema, pdforcamento:UploadFile):
    try:
        orcamento_id, mensagem = await orcamento_repo.inserir_orcamento_db(db, orcamento)
        if orcamento_id :
            return await guardar_pdf_orcamento(pdforcamento, orcamento_id)
        else:
            return False, "Erro ao inserir um orçamento"
    except Exception as e:
        return False, "Erro na inserção do orçamento, detalhes : "+str(e)

#Service para guardar um pdf associado a um orçamento
async def guardar_pdf_orcamento(pdforcamento:UploadFile, orcamento_id:int):
    try:

        load_dotenv()

        pastapdfs = os.getenv('UPLOAD_DIR_ORCAMENTO')

        orcamento_path = os.path.join(pastapdfs, str(orcamento_id))

        if not os.path.exists(orcamento_path):
            os.makedirs(orcamento_path)

        pdf_path = os.path.join(orcamento_path, pdforcamento.filename)

        with open(pdf_path,'wb+') as f:
            f.write(pdforcamento.file.read())

        return True, {'message': 'Inserção feita com sucesso'}
    except Exception as e:
        return False, {'details': str(e)}

#Service para mostrar todos os orçamentos registados
async def listar_orcamentos_service(db:session):
    try:
        load_dotenv()
        pastapdfs = os.getenv('UPLOAD_DIR_ORCAMENTO')
        orcamentos = await orcamento_repo.listar_orcamentos_db(db)
        orcamentos_caminhospdf = []
        for orcamento in orcamentos:
            orcamentos_caminhospdf.append(OrcamentoGetSchema(
                OrcamentoID = orcamento.OrcamentoID,
                Fornecedor = orcamento.Fornecedor,
                Valor = orcamento.Valor,
                DescOrcamento = orcamento.DescOrcamento,
                CaminhoPDF = os.path.join(pastapdfs, str(orcamento.OrcamentoID), orcamento.NomePDF)
                )
            )
        return orcamentos_caminhospdf
    except Exception as e:
        raise e

#Service para eliminar um orçamento
async def eliminar_orcamento_service(db:session, orcamento_id:int):
    try:
        load_dotenv()

        pastapdfs = os.getenv('UPLOAD_DIR_ORCAMENTO')

        val, msg = await orcamento_repo.eliminar_orcamento_db(db, orcamento_id)

        shutil.rmtree(os.path.join(pastapdfs, str(orcamento_id)))

        return val, msg

    except Exception as e:
        raise e

#Service para alterar os dados de um orçamento
async def alterar_orcamento_service(db:session, orcamento:OrcamentoUpdateSchema, pdforcamento:UploadFile):
    try:
        if pdforcamento: #Caso seja adicionado um novo pdf que vá substituir o antigo

            load_dotenv()

            pasta = Path(os.path.join(os.getenv('UPLOAD_DIR_ORCAMENTO'), str(orcamento.OrcamentoID)))

            if pasta:
                for item in pasta.iterdir():
                    if item.is_file():
                        os.remove(item)

            await guardar_pdf_orcamento(pdforcamento, orcamento.OrcamentoID)

        return await orcamento_repo.altera_orcamento_db(db, orcamento, pdforcamento.filename)
    except Exception as e:
        raise e