from fastapi import APIRouter, Depends, HTTPException
from services.entidade_service import registar_entidade, ver_entidades, eliminar_entidade_service, update_entidade_service
from schemas.entidade_schema import EntidadeSchema, EntidadeUpdateSchema
from middleware.auth_middleware import role_required
from schemas.user_schemas import UserJWT
from sqlalchemy.orm import Session
from db.session import get_db

router = APIRouter(prefix="/entidades", tags=["Entidades Externas"])

#Endpoint para registar uma nova entidade externa
@router.post("/registar")
async def endpoint_registar_entidade(entidade: EntidadeSchema, token: UserJWT = Depends(role_required(["admin", "gestor"])), db: Session = Depends(get_db)):
    try:
        val, msg = await registar_entidade(entidade, db)
        if val is True:
            return {"message": "Entidade registada com sucesso"}
        else:
            raise HTTPException(status_code=400, detail="Erro ao inserir a nova entidade.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Enpoint para ver as entidades externas registadas
@router.get("/ver")
async def endpoint_ver_entidades(token: UserJWT = Depends(role_required(["admin", "gestor"])), db: Session = Depends(get_db)):
    try:
        return await ver_entidades(db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Endpoint para eliminar uma entidade
@router.delete("/eliminar")
async def endpoint_eliminar_entidade(id_entidade : int,token: UserJWT = Depends(role_required(["admin", "gestor"])), db:Session = Depends(get_db)):
    try:
        return await eliminar_entidade_service(id_entidade, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Endpoint para fazer update a uma entidade externa
@router.put("/update")
async def endpoint_modificar_entidade(entidade: EntidadeUpdateSchema, token: UserJWT = Depends(role_required(["admin", "gestor"])), db:Session = Depends(get_db)):
    try:
        return await update_entidade_service(entidade, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))