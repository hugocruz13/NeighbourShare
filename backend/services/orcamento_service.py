import os
from dotenv import load_dotenv
import db.repository.orcamento_repo as orcamento_repo
import schemas.orcamento_schema as orcamentoschema
import db.session as session
from fastapi import UploadFile

async def inserir_orcamento_service(db:session, orcamento:orcamentoschema, pdforcamento:UploadFile):
    try:
        orcamento_id, mensagem = await orcamento_repo.inserir_orcamento_db(db, orcamento)
        if orcamento_id :
            return await guardar_pdf_orcamento(pdforcamento, orcamento_id)
        else:
            return False, "Erro ao inserir um orçamento"
    except Exception as e:
        return False, "Erro na inserção do orçamento, detalhes : "+str(e)

async def guardar_pdf_orcamento(pdforcamento:UploadFile, orcamento_id:int):
    try:

        load_dotenv()

        pastapdfs = os.getenv('UPLOAD_DIR')

        orcamento_path = os.path.join(pastapdfs, str(orcamento_id))

        if not os.path.exists(orcamento_path):
            os.makedirs(orcamento_path)

        pdf_path = os.path.join(orcamento_path, pdforcamento.filename)

        with open(pdf_path,'wb+') as f:
            f.write(pdforcamento.file.read())

        return True, {'message': 'Inserção feita com sucesso'}
    except Exception as e:
        return False, {'details': str(e)}
