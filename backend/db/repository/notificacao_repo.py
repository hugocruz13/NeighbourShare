from sqlalchemy.orm import Session
from db.models import Notificacao,Utilizador,TipoProcesso, TipoUtilizador, NotificacaoUser
from controllers.websockets_controller import send_notification
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

# Verifica se o tipo de processo (ID) existe
async def verifica_tipo_processo(db:Session,tipo_processo_id: int = None):
    tipo_processo = db.query(TipoProcesso).filter(TipoProcesso.TipoProcID == tipo_processo_id).first()
    if not tipo_processo:
        raise HTTPException(status_code=404, detail="Tipo de processo não existe")
    return True

#Cria uma notificação com destino somente um utilizador
async def cria_notificacao_individual_db(db: Session, notificacao: Notificacao, user_id: int = None):
    try:
        if verifica_tipo_processo(db, notificacao.TipoProcID):

            nova_notificao = Notificacao(
                Mensagem=notificacao.Mensagem,
                DataHora=datetime.now(),
                TipoProcID=notificacao.TipoProcID,
                ProcessoID=notificacao.ProcessoID,
                Estado=False
            )

            db.add(nova_notificao)
            db.commit()
            db.refresh(nova_notificao)

            db.add(NotificacaoUser(UtilizadorID=user_id, NotificacaoID=nova_notificao.NotificacaoID))
            db.commit()

            return True, {'Inserção de nova notifcação realizada com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return False ,{'details': str(e)}

# Cria notificação para somente os gestores/admins
async def cria_notificacao_admin_db(db: Session, notificacao: Notificacao):

    try:
        if verifica_tipo_processo(db, notificacao.TipoProcID):

            nova_notificao = Notificacao(
                Mensagem=notificacao.Mensagem,
                DataHora=datetime.now(),
                TipoProcID=notificacao.TipoProcID,
                ProcessoID=notificacao.ProcessoID,
                Estado=False
            )
            db.add(nova_notificao)
            db.commit()
            db.refresh(nova_notificao)

            admins = db.query(Utilizador).filter(TipoUtilizador.DescTU == 'admin')

            for admin in admins:
                db.add(NotificacaoUser(UtilizadorID=admin.UtilizadorID, NotificacaoID=nova_notificao.NotificacaoID))
                db.commit()
            return True, {'Inserção de notifcações para os admins realizada com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return False ,{'details': str(e)}

# Cria notificação para todos os utilizadores
async def cria_notificacao_todos_utilizadores_db(db:Session, notificao:Notificacao):
    try:
        if verifica_tipo_processo(db, notificao.TipoProcID):
            nova_notificao = Notificacao(
                Mensagem=notificao.Mensagem,
                DataHora=datetime.now(),
                TipoProcID=notificao.TipoProcID,
                ProcessoID=notificao.ProcessoID,
                Estado=False
            )
            db.add(nova_notificao)
            db.commit()
            db.refresh(nova_notificao)

            utilizadores = db.query(Utilizador).all()

            for utilizador in utilizadores:
                db.add(NotificacaoUser(UtilizadorID=utilizador.UtilizadorID, NotificacaoID=nova_notificao.NotificacaoID))
                db.commit()

            return True, {'Inserção de notifcações para todos os utilizadores realizada com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        return False ,{'details': str(e)}

# Lista as notificações de um utilizador por ordem descrescente de data
async def listar_notificacoes_db(db: Session, user_id: int = None):
    try:
        lista_notificacoes = (
            db.query(Notificacao)
            .filter(NotificacaoUser.UtilizadorID == user_id)
            .join(NotificacaoUser)
            .order_by(Notificacao.DataHora.desc())
        )
        return lista_notificacoes
    except SQLAlchemyError as e:
        raise SQLAlchemyError(str(e))

