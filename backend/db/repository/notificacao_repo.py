from sqlalchemy.orm import Session
from db.models import Notificacao,Utilizador,TipoProcesso, TipoUtilizador, NotificacaoUser
from controllers.websockets_controller import send_notification
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

async def cria_notificacao_db(db: Session, notificacao: Notificacao, user_id: int = None):

    try:
        tipo_processo = db.query(TipoProcesso).filter(TipoProcesso.TipoProcID == notificacao.TipoProcID).first()
        if not tipo_processo:
            raise HTTPException(status_code=404, detail="Tipo de processo não existe")

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

        utilizadores_ids = []

        if tipo_processo.DescTipoProcesso == 'Individual' and user_id:
            utilizador = db.query(Utilizador).filter(Utilizador.UtilizadorID == user_id).first()
            if utilizador:
                utilizadores_ids = [utilizador.UtilizadorID]
        elif tipo_processo.DescTipoProcesso == 'Todos':
            utilizadores_ids = [u[0] for u in db.query(Utilizador.UtilizadorID).all()]
        elif tipo_processo.DescTipoProcesso == 'Gestores':
            utilizadores_ids = [u[0] for u in db.query(Utilizador.UtilizadorID).filter(TipoUtilizador.DescTU == 'Gestor').all()]

        for utilizadorID in utilizadores_ids:
            nova_relacao = NotificacaoUser(NotificacaoID=nova_notificao.NotificacaoID, UtilizadorID=utilizadorID)
            db.add(nova_relacao)
            await send_notification(utilizadorID, nova_notificao.Mensagem)
        db.commit()
        return True, {'Inserção e envio de notificação realizada com sucesso'}
    except SQLAlchemyError as e:
        db.rollback()
        return False ,{'details': str(e)}