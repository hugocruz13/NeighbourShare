import db.repository.orcamento_repo as orcamento_repo
import schemas.orcamento_schema as orcamentoschema
import db.session as session

async def inserir_orcamento_service(db:session, orcamento:orcamentoschema):
    try:
        if await orcamento_repo.inserir_orcamento_db(db, orcamento):
            return True, "Sucesso ao inserir um orçamento"
        else:
            return False, "Erro ao inserir um orçamento"
    except Exception as e:
        return False, "Erro na inserção do orçamento, detalhes : "+str(e)
