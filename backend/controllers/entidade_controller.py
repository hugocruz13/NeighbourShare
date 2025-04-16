from fastapi import APIRouter, Depends, HTTPException
from services.entidade_service import registar_entidade, ver_entidades
from schemas.entidade_schema import EntidadeSchema
from middleware.auth_middleware import role_required
from schemas.user_schemas import UserJWT
from sqlalchemy.orm import Session
from db.session import get_db

router = APIRouter(prefix="/entidades", tags=["Entidades Externas"])

@router.post("/registar")
async def endpoint_registar_entidade(entidade: EntidadeSchema, token: UserJWT = Depends(role_required(["admin", "gestor"])), db: Session = Depends(get_db)):
    try:
        val, msg = await registar_entidade(entidade, db)
        if val is True:
            return {"message": "Entidade registada com sucesso"}
    except HTTPException as h:
        raise h
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})

@router.get("/ver")
async def endpoint_ver_entidades(token: UserJWT = Depends(role_required(["admin", "gestor"])), db: Session = Depends(get_db)):
    try:
        return await ver_entidades(db)
    except HTTPException as e:
        raise HTTPException(status_code=500, detail={str(e)})