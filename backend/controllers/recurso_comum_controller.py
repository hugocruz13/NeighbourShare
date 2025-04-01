from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.schemas.recurso_comum_schema import PedidoNovoRecursoSchema, PedidoManutencaoSchema
from backend.services.recurso_comum_service import *
from typing import Union, Dict, List
from pydantic import BaseModel

class ResponseModelTuple(BaseModel):
    success: bool
    data: Dict[str, str]

ResponseModelPedidoNovoRecurso = Union[ResponseModelTuple, List[PedidoNovoRecursoSchema]]
ResponseModelPedidoManutencao = Union[ResponseModelTuple, List[PedidoManutencaoSchema]]

router = APIRouter(prefix="/recursoscomum", tags=["Recursos Comuns"])

@router.get("/pedidosnovos", response_model=ResponseModelPedidoNovoRecurso)
def listar_pedidos_novos_recursos(
        db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de novos recursos comuns
    """
    return listar_pedidos_novos_recursos_service(db)

@router.get("/pedidosnovos/pendentes", response_model=ResponseModelPedidoNovoRecurso)
def listar_pedidos_novos_recursos_pendentes(
        db: Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de novos recursos comuns pendentes (EstadoPedidoNovoRec == 1)
    """
    return listar_pedidos_novos_recursos_pendentes(db)

@router.get("/pedidosnovos/aprovados", response_model=ResponseModelPedidoNovoRecurso)
def listar_pedidos_novos_recursos_aprovados(
        db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de novos recursos comuns aprovados (EstadoPedidoNovoRec == 2)
    """
    return listar_pedidos_novos_recursos_aprovados(db)

@router.get("/pedidosmanutencao", response_model=ResponseModelPedidoManutencao)
def listar_pedidos_manutencao(
        db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de manutenção de recursos comuns
    """

    return listar_pedidos_manutencao(db)


@router.get("/pedidosmanutencao/progresso", response_model=ResponseModelPedidoManutencao)
def listar_pedidos_manutencao_em_progresso(
        db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de manutenção de recursos comuns em progresso (EstadoPedManuID == 1)
    """

    return listar_pedidos_manutencao_em_progresso(db)

@router.get("/pedidosmanutencao/finalizados", response_model=ResponseModelPedidoManutencao)
def listar_pedidos_manutencao_finalizados(
        db:Session = Depends(get_db)
):
    """
    Endpoint para consultar todos os pedidos de manutenção de recursos comuns em progresso (EstadoPedManuID == 2)
    """

    return listar_pedidos_manutencao_finalizados(db)