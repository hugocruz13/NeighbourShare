from schemas.entidade_schema import EntidadeSchema
from db.session import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from db.repository.entidade_repo import inserir_entidade_db, visualizar_entidades_db

async def registar_entidade(entidade: EntidadeSchema, db: Session = Depends(get_db)):
    try:
        val, msg = await inserir_entidade_db(db, entidade)
        if val is False:
            raise HTTPException(status_code=400, detail=msg)
        else:
            return True, msg
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def ver_entidades(db: Session = Depends(get_db)):
    try:
        return await visualizar_entidades_db(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))