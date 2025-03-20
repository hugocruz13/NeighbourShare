from fastapi import APIRouter, Depends
from services.auth_service import registar_utilizador
from schemas.user_schemas import UserRegistar
from db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/registar")
def registar(user:UserRegistar, db: Session = Depends(get_db)):
    return  registar_utilizador(db, user)

#@router.post("/", response_model=UserResponse)
#def get_user(user_email:UserBase, db: Session = Depends(get_db)):
#    return get_user_by_email(db, user_email)