from fastapi import FastAPI,Depends, HTTPException,APIRouter
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.models.models import Notificacao,Utilizador,t_NotificacaoUser,TipoProcesso, TipoUtilizador
from backend.controllers.websockets_controller import send_notification
from datetime import datetime

app = FastAPI()

router = APIRouter(tags=["Notificacao"])

@app.post("/notificacao/")
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

    utilizadores_notificacao = []

    if tipo_processo.DescTipoProcesso == 'Individual' and user_id:
        utilizador = db.query(Utilizador).filter(Utilizador.UtilizadorID == user_id).first()
        if utilizador:
            utilizadores_notificacao.append(utilizador)
    elif tipo_processo.DescTipoProcesso == 'Todos':
        utilizadores_notificacao = db.query(Utilizador).all()
    elif tipo_processo.DescTipoProcesso == 'Gestores':
        utilizadores_notificacao = db.query(Utilizador).filter(TipoUtilizador.DescTU == 'Gestor').all()

    for utilizador in utilizadores_notificacao:
        nova_relacao = t_NotificacaoUser(NotificacaoID=nova_notificao.NotificacaoID, UtilizadorID=utilizador.UtilizadorID)
        db.add(nova_relacao)
        await send_notification(utilizador.UtilizadorID, nova_notificao.Mensagem)

    db.commit()
    return {"status": "Nova notificação enviadad com sucesso"}
