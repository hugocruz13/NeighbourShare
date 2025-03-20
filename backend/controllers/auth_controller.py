import schemas
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from db.session import get_db
from schemas import *
from typing import Optional
from services.auth_service import registar_utilizador

router = APIRouter()


@router.post("/registar")
async def registar(user: UserRegistar = Depends(), foto: Optional[UploadFile] = File(None), db: Session = Depends(get_db)):
    try:
        if await registar_utilizador(user, foto, db):
            return {"message": "Registo realizado com sucesso"}
        else:
            return {"message": "Cliente já está registado"}
    except Exception as e:
        return {"error": str(e)}



#@router.post("/", response_model=UserResponse)
#def get_user(user_email:UserBase, db: Session = Depends(get_db)):
#    return get_user_by_email(db, user_email)