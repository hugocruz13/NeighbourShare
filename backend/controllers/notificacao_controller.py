from fastapi import Depends, HTTPException,APIRouter

from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.models.models import Notificacao,Utilizador,TipoProcesso, TipoUtilizador, NotificacaoUser
from backend.controllers.websockets_controller import send_notification
from datetime import datetime

router = APIRouter(tags=["Notificacao"])

@router.post("/notificacao/")
async def cria_notificacao(
    mensagem: str,
    processoid : int,
    tipoprocessoid : int,
    user_id: int = None,
    db:Session = Depends(get_db)
):
    tipo_processo = db.query(TipoProcesso).filter(TipoProcesso.TipoProcID == tipoprocessoid).first()
    if not tipo_processo:
        raise HTTPException(status_code=404, detail= "Tipo de processo não existe")

    nova_notificao = Notificacao(
        Mensagem=mensagem,
        DataHora= datetime.now(),
        TipoProcID=tipoprocessoid,
        ProcessoID=processoid,
        Estado = False
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
        utilizadores_ids =  [u[0] for u in db.query(Utilizador.UtilizadorID).filter(TipoUtilizador.DescTU == 'Gestor').all()]

    for utilizadorID in utilizadores_ids:
        nova_relacao = NotificacaoUser(NotificacaoID=nova_notificao.NotificacaoID, UtilizadorID=utilizadorID)
        db.add(nova_relacao)
        await send_notification(utilizadorID, nova_notificao.Mensagem)
    db.commit()
    return {"status": "Nova notificação enviada com sucesso"}
