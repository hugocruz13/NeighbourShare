from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.recurso_comum_schema import PedidoNovoRecursoSchema, PedidoManutencaoSchema
from services.recurso_comum_service import *
from typing import List

router = APIRouter(prefix="/recursoscomum", tags=["Recursos Comuns"])

@router.get("/pedidosnovos", response_model=List[PedidoNovoRecursoSchema])
async def listar_pedidos_novos_recursos(
        db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de novos recursos comuns
    """
    return await listar_pedidos_novos_recursos_service(db)

@router.get("/pedidosnovos/pendentes", response_model=List[PedidoNovoRecursoSchema])
async def listar_pedidos_novos_recursos_pendentes(
        db: Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de novos recursos comuns pendentes (EstadoPedidoNovoRec == 1)
    """
    return await listar_pedidos_novos_recursos_pendentes_service(db)

@router.get("/pedidosnovos/aprovados", response_model=List[PedidoNovoRecursoSchema])
async def listar_pedidos_novos_recursos_aprovados(
        db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de novos recursos comuns aprovados (EstadoPedidoNovoRec == 2)
    """
    return await listar_pedidos_novos_recursos_aprovados_service(db)

@router.get("/pedidosmanutencao", response_model=List[PedidoManutencaoSchema])
async def listar_pedidos_manutencao(
        db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de manutenção de recursos comuns
    """

    return await listar_pedidos_manutencao_service(db)


@router.get("/pedidosmanutencao/progresso", response_model=List[PedidoManutencaoSchema])
async def listar_pedidos_manutencao_em_progresso(
        db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de manutenção de recursos comuns em progresso (EstadoPedManuID == 1)
    """

    return await listar_pedidos_manutencao_em_progresso_service(db)

@router.get("/pedidosmanutencao/finalizados", response_model=List[PedidoManutencaoSchema])
async def listar_pedidos_manutencao_finalizados(
        db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de manutenção de recursos comuns em progresso (EstadoPedManuID == 2)
    """

    return await listar_pedidos_manutencao_finalizados_service(db)