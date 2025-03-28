from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from backend.db.session import get_db
from backend.models.models import PedidoNovoRecurso, PedidoManutencao
from backend.schemas.recurso_comum_schema import PedidoNovoRecursoSchema, PedidoManutencaoSchema

router = APIRouter(prefix="/recursoscomum", tags=["Recursos Comuns"])

@router.get("/pedidosnovos", response_model=List[PedidoNovoRecursoSchema])
def listar_pedidos_novos_recursos(
        db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de novos recursos comuns
    """
    pedidos_novos_recursos = (
        db.query(PedidoNovoRecurso)
        .options(
            joinedload(PedidoNovoRecurso.Utilizador_),
            joinedload(PedidoNovoRecurso.EstadoPedidoNovoRecurso_)
        )
        .all()
    )

    if not pedidos_novos_recursos:
        raise HTTPException(status_code=404, detail="Nenhum pedido de novo recurso encontrado")

    return pedidos_novos_recursos

@router.get("/pedidosnovos/pendentes", response_model=List[PedidoNovoRecursoSchema])
def listar_pedidos_novos_recursos_pendentes(
        db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de novos recursos comuns pendentes (EstadoPedidoNovoRec == 1)
    """
    pedidos_novos_recursos_pendentes = (
        db.query(PedidoNovoRecurso)
        .options(
            joinedload(PedidoNovoRecurso.Utilizador_),
            joinedload(PedidoNovoRecurso.EstadoPedidoNovoRecurso_)
        )
        .filter(PedidoNovoRecurso.EstadoPedNovoRecID == 1)
        .all()
    )

    if not pedidos_novos_recursos_pendentes:
        raise HTTPException(status_code=404, detail="Nenhum pedido de um novo recurso pendente encontrado")

    return pedidos_novos_recursos_pendentes

@router.get("/pedidosnovos/aprovado", response_model=List[PedidoNovoRecursoSchema])
def listar_pedidos_novos_recursos_aprovado(
        db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de novos recursos comuns aprovados (EstadoPedidoNovoRec == 2)
    """
    pedidos_novos_recursos_aprovados = (
        db.query(PedidoNovoRecurso)
        .options(
            joinedload(PedidoNovoRecurso.Utilizador_),
            joinedload(PedidoNovoRecurso.EstadoPedidoNovoRecurso_)
        )
        .filter(PedidoNovoRecurso.EstadoPedNovoRecID == 2)
        .all()
    )

    if not pedidos_novos_recursos_aprovados:
        raise HTTPException(status_code=404, detail="Nenhum pedido de um novo recurso aceite encontrado")

    return pedidos_novos_recursos_aprovados

@router.get("/pedidosmanutencao", response_model=List[PedidoManutencaoSchema])
def listar_pedidos_manutencao(
        db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de manutenção de recursos comuns
    """

    pedidos_manutencao = (
        db.query(PedidoManutencao)
        .options(
            joinedload(PedidoManutencao.Utilizador_),
            joinedload(PedidoManutencao.EstadoPedidoManutencao_),
            joinedload(PedidoManutencao.RecursoComun_)
        )
        .all()
    )

    if not pedidos_manutencao:
        raise HTTPException(status_code=404, detail="Nenhum pedido de manutenção encontrado")

    return pedidos_manutencao


@router.get("/pedidosmanutencao/progresso", response_model=List[PedidoManutencaoSchema])
def listar_pedidos_manutencao_em_progresso(
        db: Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de manutenção de recursos comuns em progresso (EstadoPedManuID == 1)
    """

    pedidos_manutencao_em_progresso = (
        db.query(PedidoManutencao)
        .options(
            joinedload(PedidoManutencao.Utilizador_),
            joinedload(PedidoManutencao.EstadoPedidoManutencao_),
            joinedload(PedidoManutencao.RecursoComun_)
        )
        .filter(PedidoManutencao.EstadoPedManuID == 1)
        .all()
    )

    if not pedidos_manutencao_em_progresso:
        raise HTTPException(status_code=404, detail="Nenhum pedido de manutenção em progresso encontrado")

    return pedidos_manutencao_em_progresso

@router.get("/pedidosmanutencao/finalizado", response_model=List[PedidoManutencaoSchema])
def listar_pedidos_manutencao_finalizado(
        db: Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de manutenção de recursos comuns em progresso (EstadoPedManuID == 2)
    """

    pedidos_manutencao_finalizado = (
        db.query(PedidoManutencao)
        .options(
            joinedload(PedidoManutencao.Utilizador_),
            joinedload(PedidoManutencao.EstadoPedidoManutencao_),
            joinedload(PedidoManutencao.RecursoComun_)
        )
        .filter(PedidoManutencao.EstadoPedManuID == 2)
        .all()
    )

    if not pedidos_manutencao_finalizado:
        raise HTTPException(status_code=404, detail="Nenhum pedido de manutenção em progresso encontrado")

    return pedidos_manutencao_finalizado