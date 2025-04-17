from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.recurso_comum_schema import PedidoNovoRecursoSchema, PedidoManutencaoSchema
from services.recurso_comum_service import *
from typing import List
from middleware.auth_middleware import *

router = APIRouter(prefix="/recursoscomuns", tags=["Recursos Comuns"])

#Inserção de um novo recurso comum
@router.post("/inserir")
async def inserir_recurso_comum(recurso:RecursoComumSchemaCreate, db:Session = Depends(get_db)):
    return await inserir_recurso_comum_service(db, recurso)

#Inserção de um pedido de um novo recurso comum
@router.post("/pedidosnovos/inserir")
async def inserir_recurso_comum(desc_pedido_novo_recurso: str, db:Session = Depends(get_db),  token: UserJWT = Depends(jwt_middleware)):
    novo_pedido = PedidoNovoRecursoSchemaCreate(
        DescPedidoNovoRecurso=desc_pedido_novo_recurso,
        UtilizadorID=token.id,
        DataPedido = date.today(),
        EstadoPedNovoRecID= 1 # Referente ao estado 'Pendente'
    )

    return await inserir_pedido_novo_recurso_service(db,novo_pedido)

#Inserção de um pedido de manutenção de um recurso comum
@router.post("/pedidosmanutencao/inserir")
async def inserir_manutencao_recurso_comum(recurso_comum_id: int, desc_manutencao_recurso_comum: str,   token: UserJWT = Depends(jwt_middleware),  db:Session = Depends(get_db)):

    novo_pedido_manutencao = PedidoManutencaoSchemaCreate(
        UtilizadorID=token.id,
        RecComumID=recurso_comum_id,
        DescPedido=desc_manutencao_recurso_comum,
        DataPedido = date.today(),
        EstadoPedManuID= 1 # Relativo ao estado 'Em análise'
    )

    return await inserir_pedido_manutencao_service(db, novo_pedido_manutencao)

@router.get("/pedidosnovos", response_model=List[PedidoNovoRecursoSchema])
async def listar_pedidos_novos_recursos(db:Session = Depends(get_db)):
    """
    Endpoint para consultar todos os pedidos de novos recursos comuns
    """
    return await listar_pedidos_novos_recursos_service(db)

@router.get("/pedidosnovos/pendentes", response_model=List[PedidoNovoRecursoSchema])
async def listar_pedidos_novos_recursos_pendentes(db: Session = Depends(get_db)):
    """
    Endpoint para consultar todos os pedidos de novos recursos comuns pendentes (EstadoPedidoNovoRec == 1)
    """
    return await listar_pedidos_novos_recursos_pendentes_service(db)

@router.get("/pedidosnovos/aprovados", response_model=List[PedidoNovoRecursoSchema])
async def listar_pedidos_novos_recursos_aprovados(db:Session = Depends(get_db)):
    """
    Endpoint para consultar todos os pedidos de novos recursos comuns aprovados (EstadoPedidoNovoRec == 2)
    """
    return await listar_pedidos_novos_recursos_aprovados_service(db)

@router.get("/pedidosmanutencao", response_model=List[PedidoManutencaoSchema])
async def listar_pedidos_manutencao(db:Session = Depends(get_db)):
    """
    Endpoint para consultar todos os pedidos de manutenção de recursos comuns
    """
    return await listar_pedidos_manutencao_service(db)


@router.get("/pedidosmanutencao/progresso", response_model=List[PedidoManutencaoSchema])
async def listar_pedidos_manutencao_em_progresso(db:Session = Depends(get_db)):
    """
    Endpoint para consultar todos os pedidos de manutenção de recursos comuns em progresso (EstadoPedManuID == 1)
    """

    return await listar_pedidos_manutencao_em_progresso_service(db)

@router.get("/pedidosmanutencao/finalizados", response_model=List[PedidoManutencaoSchema])
async def listar_pedidos_manutencao_finalizados(db:Session = Depends(get_db)):
    """
    Endpoint para consultar todos os pedidos de manutenção de recursos comuns em progresso (EstadoPedManuID == 2)
    """
    return await listar_pedidos_manutencao_finalizados_service(db)