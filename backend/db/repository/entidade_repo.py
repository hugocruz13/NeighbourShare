from sqlalchemy.orm import Session
from db.models import EntidadeExterna
from schemas.entidade_schema import EntidadeSchema
from sqlalchemy.exc import SQLAlchemyError

async def inserir_entidade_db(db: Session, entidade: EntidadeSchema):
    try:
        nova_entidade = EntidadeExterna(
            Especialidade=entidade.Especialidade,
            Nome=entidade.Nome,
            Email=str(entidade.Email),
            Contacto=entidade.Contacto,
            Nif=entidade.Nif
        )
        db.add(nova_entidade)
        db.commit()
        db.refresh(nova_entidade)

        return True, {'Nova entidade inserida com sucesso.'}
    except SQLAlchemyError as e:
        db.rollback()
        return False, {'details': str(e)}

async def visualizar_entidades_db(db: Session):
    try:
        entidades = db.query(EntidadeExterna).all()
        return entidades
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))