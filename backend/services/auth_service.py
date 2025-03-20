from sqlalchemy.orm import Session
from schemas import UserRegistar
from db.repository.user_repo import get_id_role, create_user, user_exists
from fastapi import UploadFile


async def registar_utilizador(user: UserRegistar, foto: UploadFile,db: Session):
    try:

        #Converte a imagem inserida ou defaut
        if foto is not None:
            foto_bytes = await foto.read()
        else:
            with open("img/default.png", "rb") as default_file:
                foto_bytes = default_file.read()

        # Remove os espaços
        user.role = FormatarString(user.role)
        user.email = FormatarString(user.email)
        # user.password = HASH_PASSWORD
        salt = "Obter salt"

        # verificar se o email já existe
        if await user_exists(db, user.email):
            return False
        else:
            role_id = await get_id_role(db, user.role)
            create_user(db, user, role_id, salt, foto_bytes)
            return True

    except Exception as e:
        print(e)
        return {"error": str(e)}


def FormatarString(word:str):
    return word.strip()
