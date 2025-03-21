from sqlalchemy.orm import Session
from schemas import UserRegistar
from db.repository.user_repo import get_id_role, create_user, user_exists

async def registar_utilizador(user: UserRegistar,db: Session):
    try:
        # Remove os espaços
        user.role = FormatarString(user.role)
        user.email = FormatarString(user.email)
        # user.password = HASH_PASSWORD
        salt = "Obter salt"

        # TODO: VER PORQUÊ QUE DÁ SEMPRE REGISTADO COM SUCESSO MESMO QUE NÃO TENHA INSERIDO NA BASE DE DADOS!!
        if await user_exists(db, user.email):
            return False
        else:
            role_id = await get_id_role(db, user.role)
            create_user(db, user, role_id, salt)
            return True

    except Exception as e:
        print(e)
        return {"error": str(e)}


def FormatarString(word:str):
    return word.strip()
