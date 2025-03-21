from sqlalchemy.orm import Session
from schemas import UserRegistar
from db.repository.user_repo import get_id_role, create_user, user_exists

async def registar_utilizador(user: UserRegistar, db: Session):
    try:
        # Remove os espaços
        user.role = FormatarString(user.role)
        user.email = FormatarString(user.email)

        # Verifica se usuário já existe
        if await user_exists(db, user.email):
            return False, "Email já está em uso"

        # Obtém ID do papel (role)
        role_id = await get_id_role(db, user.role)
        if role_id is None:
            return False, "Role não encontrado"

        # Define um salt (você precisa implementar isso corretamente)
        salt = "Obter salt"

        # Criação do usuário
        if await create_user(db, user, role_id, salt):
            return True, "Usuário criado com sucesso"
        else:
            return False, "Erro ao criar usuário"

    except Exception as e:
        raise RuntimeError(f"Erro em registar_utilizador: {e}")


def FormatarString(word:str):
    return word.strip()
