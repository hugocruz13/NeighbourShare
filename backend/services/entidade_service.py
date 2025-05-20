from schemas.entidade_schema import EntidadeSchema, EntidadeUpdateSchema
from db.session import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from db.repository.entidade_repo import inserir_entidade_db, visualizar_entidades_db, update_entidade_db, \
    remover_entidade_db, existe_entidade_db

#Service para registar uma nova entidade externa
async def registar_entidade(entidade: EntidadeSchema, db: Session = Depends(get_db)):
    try:
        val = await inserir_entidade_db(db, entidade)
        if val is None:
            raise HTTPException(status_code=400, detail="Erro ao inserir a nova entidade.")
        else:
            return val
    except HTTPException as e:
            raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Service para ver todas as entidades registadas no sistema
async def ver_entidades(db: Session = Depends(get_db)):
    try:
        return await visualizar_entidades_db(db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Service para eliminar uma entidade externa
async def eliminar_entidade_service(id_entidade: int, db: Session = Depends(get_db)):
    try:
        if not await existe_entidade_db(id_entidade,db):
            raise HTTPException(status_code=404, detail="Entidade não existe")
        val, msg = await remover_entidade_db(id_entidade, db)

        if val is False:
            raise HTTPException(status_code=400, detail="Entidade não existe ou é inválido")
        else:
            return True, msg
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Service para realizar um update a uma entidade externa
async def update_entidade_service(entidade: EntidadeUpdateSchema, db: Session = Depends(get_db)):
    try:
        if not await existe_entidade_db(entidade.EntidadeID,db):
            raise HTTPException(status_code=404, detail="Entidade não existe")
        val, msg = await update_entidade_db(entidade, db)
        if val is False:
            raise HTTPException(status_code=400, detail="Erro ao alterar os dados da entidade!")
        else:
            return True, msg
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
