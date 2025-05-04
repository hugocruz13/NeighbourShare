from sqlalchemy.orm import Session, aliased
from db.models import Notificacao,Utilizador,TipoProcesso, TipoUtilizador, t_NotificacaoUser
import datetime
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from schemas.notificacao_schema import *

#Cria uma notificação com destino somente um utilizador
async def cria_notificacao_individual_db(db: Session, notificacao: NotificacaoSchema, user_id: int = None):
    try:
            nova_notificao = Notificacao(
                Titulo=notificacao.Titulo,
                Mensagem=notificacao.Mensagem,
                DataHora=datetime.datetime.now(),
                TipoProcID=notificacao.TipoProcessoID,
                ProcessoID=notificacao.ProcessoID,
                Estado=False
            )

            db.add(nova_notificao)
            db.commit()
            db.refresh(nova_notificao)

            db.execute(t_NotificacaoUser.insert().values(UtilizadorID=user_id, NotificacaoID=nova_notificao.NotificacaoID))
            db.commit()
            db.refresh(nova_notificao)
            return True, {'Inserção de nova notifcação realizada com sucesso!'}, nova_notificao
    except SQLAlchemyError as e:
        db.rollback()
        return False ,{'details': str(e)}, None

# Cria notificação para somente os gestores/admins
async def cria_notificacao_admin_db(db: Session, notificacao: NotificacaoSchema):
    try:
            nova_notificao = Notificacao(
                Titulo=notificacao.Titulo,
                Mensagem=notificacao.Mensagem,
                DataHora=datetime.datetime.now(),
                TipoProcID=notificacao.TipoProcessoID,
                ProcessoID=notificacao.ProcessoID,
                Estado=False
            )
            db.add(nova_notificao)
            db.commit()
            db.refresh(nova_notificao)

            admins = db.query(Utilizador).filter(TipoUtilizador.DescTU == 'admin')

            for admin in admins:
                db.execute(
                    t_NotificacaoUser.insert().values(UtilizadorID=admin.UtilizadorID, NotificacaoID=nova_notificao.NotificacaoID))
                db.commit()
            return True, {'Inserção de notificações para os admins realizada com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return False ,{'details': str(e)}

# Cria notificação para todos os utilizadores
async def cria_notificacao_todos_utilizadores_db(db:Session, notificao:NotificacaoSchema):
    try:
            nova_notificao = Notificacao(
                Titulo=notificao.Titulo,
                Mensagem=notificao.Mensagem,
                DataHora=datetime.datetime.now(),
                TipoProcID=notificao.TipoProcessoID,
                ProcessoID=notificao.ProcessoID,
                Estado=False
            )
            db.add(nova_notificao)
            db.commit()
            db.refresh(nova_notificao)

            utilizadores = db.query(Utilizador).all()

            for utilizador in utilizadores:
                db.execute(
                    t_NotificacaoUser.insert().values(UtilizadorID=utilizador.UtilizadorID, NotificacaoID=nova_notificao.NotificacaoID))
                db.commit()

            return True, {'Inserção de notifcações para todos os utilizadores realizada com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return False ,{'details': str(e)}

# Lista as notificações de um utilizador por ordem descrescente de data
async def listar_notificacoes_db(db: Session, user_id: int):
    try:
        notificacao_user_alias = aliased(t_NotificacaoUser)
        lista_notificacoes = (
            db.query(Notificacao)
            .join(notificacao_user_alias, Notificacao.NotificacaoID == notificacao_user_alias.c.NotificacaoID)
            .filter(notificacao_user_alias.c.UtilizadorID == user_id)
            .order_by(Notificacao.DataHora.desc())
        )
        return lista_notificacoes
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

#Marcar uma notificação como lida
async def marcar_notificacao_lida_db(db: Session, notificacao_id: int):
    try:
        notificacao = db.query(Notificacao).filter(Notificacao.NotificacaoID == notificacao_id).first()
        notificacao.Estado = True
        db.commit()
        db.refresh(notificacao)

        return {'Notificação marcada como lida!'}
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

#Obtêm o id de um tipo de processo a associar a uma notificação
async def get_tipo_processo_id(db:Session, tipoprocesso: TipoProcessoOpcoes):
    try:
        resultado = db.query(TipoProcesso.TipoProcID) \
            .filter(TipoProcesso.DescTipoProcesso == tipoprocesso.value) \
            .first()
        if resultado is not None:
            return int(resultado.TipoProcID)
        else:
            raise ValueError("Tipo de processo não encontrado.")
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

