from sqlalchemy.orm import Session
from schemas import UserRegistar
from db.repository.user_repo import get_id_role, create_user, user_exists
from utils.PasswordHasher import hash_password

async def registar_utilizador(user: UserRegistar, db: Session):
    try:
        # Remove os espaços
        user.role = formatar_string(user.role)
        user.email = formatar_string(user.email)

        # Verifica se o utilizador já existe
        if await user_exists(db, user.email):
            return False, "Email já está em uso"

        # Obtém ID do cargo
        role_id = await get_id_role(db, user.role)
        if role_id is None:
            return False, "Cargo não encontrado"

        user.password, salt = hash_password(user.password)

        # Adicionar o utilizador na base de dados
        if await create_user(db, user, role_id, salt):
            return True, "Utilizador criado com sucesso"
        else:
            return False, "Erro ao criar o Utilizador"

    except Exception as e:
        raise RuntimeError(f"Erro registar_utilizador: {e}")


def formatar_string(word:str):
    return word.strip()
