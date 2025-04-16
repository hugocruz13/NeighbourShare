from datetime import date
from fastapi import APIRouter, Depends
from db.session import get_db
from services.recurso_comum_service import *
from middleware.auth_middleware import *
from schemas.user_schemas import UserJWT

router = APIRouter(prefix="/recursoscomuns", tags=["Recursos Comuns"])

#Inserção de um novo recurso comum
@router.post("/inserir")
async def inserir_recurso_comum(
        nome_recurso:str,
        descricao_recurso:str,
        db:Session = Depends(get_db)
):
    novo_recurso_comum = RecursoComumSchemaCreate(
        Nome=nome_recurso,
        DescRecursoComum=descricao_recurso
    )

    return await inserir_recurso_comum_service(db, novo_recurso_comum)

#Inserção de um pedido de um novo recurso comum
@router.post("/pedidosnovos/inserir")
async def inserir_pedido_novo_recurso_comum(
    desc_pedido_novo_recurso: str,
    db:Session = Depends(get_db),
    token: UserJWT = Depends(jwt_middleware)
):
    novo_pedido = PedidoNovoRecursoSchemaCreate(
        DescPedidoNovoRecurso=desc_pedido_novo_recurso,
        UtilizadorID=token.id,
        DataPedido = date.today(),
        EstadoPedNovoRecID= 1 # Referente ao estado 'Pendente'
    )

    return await inserir_pedido_novo_recurso_service(db,novo_pedido)

#Inserção de um pedido de manutenção de um recurso comum
@router.post("/pedidosmanutencao/inserir")
async def inserir_manutencao_recurso_comum(
    recurso_comum_id: int,
    desc_manutencao_recurso_comum: str,
    token: UserJWT = Depends(jwt_middleware),
    db:Session = Depends(get_db)
):
    novo_pedido_manutencao = PedidoManutencaoSchemaCreate(
        UtilizadorID=token.id,
        RecComumID=recurso_comum_id,
        DescPedido=desc_manutencao_recurso_comum,
        DataPedido = date.today(),
        EstadoPedManuID= 1 # Relativo ao estado 'Em análise'
    )

    return await inserir_pedido_manutencao_service(db, novo_pedido_manutencao)

@router.get("/pedidosnovos", response_model=List[PedidoNovoRecursoSchema])
async def listar_pedidos_novos_recursos(
        db:Session = Depends(get_db),
        token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))
):
    """
    Endpoint para consultar todos os pedidos de novos recursos comuns
    """
    return await listar_pedidos_novos_recursos_service(db)

@router.get("/pedidosnovos/pendentes", response_model=List[PedidoNovoRecursoSchema])
async def listar_pedidos_novos_recursos_pendentes(
        db: Session = Depends(get_db),
        token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))
):
    """
    Endpoint para consultar todos os pedidos de novos recursos comuns pendentes (EstadoPedidoNovoRec == 1)
    """
    return await listar_pedidos_novos_recursos_pendentes_service(db)

@router.get("/pedidosnovos/aprovados", response_model=List[PedidoNovoRecursoSchema])
async def listar_pedidos_novos_recursos_aprovados(
        db:Session = Depends(get_db),
        token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))
):
    """
    Endpoint para consultar todos os pedidos de novos recursos comuns aprovados (EstadoPedidoNovoRec == 2)
    """
    return await listar_pedidos_novos_recursos_aprovados_service(db)

@router.get("/pedidosmanutencao", response_model=List[PedidoManutencaoSchema])
async def listar_pedidos_manutencao(
        db:Session = Depends(get_db),
    token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))
):
    """
    Endpoint para consultar todos os pedidos de manutenção de recursos comuns
    """

    return await listar_pedidos_manutencao_service(db)


@router.get("/pedidosmanutencao/progresso", response_model=List[PedidoManutencaoSchema])
async def listar_pedidos_manutencao_em_progresso(
        db:Session = Depends(get_db),
        token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))
):
    """
    Endpoint para consultar todos os pedidos de manutenção de recursos comuns em progresso (EstadoPedManuID == 1)
    """

    return await listar_pedidos_manutencao_em_progresso_service(db)

@router.get("/pedidosmanutencao/finalizados", response_model=List[PedidoManutencaoSchema])
async def listar_pedidos_manutencao_finalizados(
        db:Session = Depends(get_db),
        token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))
):
    """
    Endpoint para consultar todos os pedidos de manutenção de recursos comuns em progresso (EstadoPedManuID == 2)
    """

    return await listar_pedidos_manutencao_finalizados_service(db)

@router.get("/manutencao/", response_model=List[ManutencaoSchema])
async def listar_manutencoes(db:Session = Depends(get_db), token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))):
    return await visualizar_manutencoes(db)

@router.get("/pedidodsmanutencao/estados")
async def listar_tipos_pedido_manutencao(db:Session = Depends(get_db), token: UserJWT=Depends(role_required(["admin", "residente", "gestor"]))):
    return await obter_all_tipo_estado_pedido_manutencao(db)

@router.get("/manutencao/estados")
async def listar_tipos_manutencao(db: Session = Depends(get_db), token:UserJWT=Depends(role_required(["admin", "residente", "gestor"]))):
    return await obter_all_tipo_estado_manutencao(db)

@router.put("/pedidosmanutencao/{pedido_id}/estado")
async def atualizar_estado_pedido(pedido_id: int, estado_data: EstadoUpdate, db: Session = Depends(get_db)):
    try:
        obter = await obter_pedido_manutencao(db, pedido_id)
        if obter is None:
            raise HTTPException(status_code=404, detail="Pedido de manutenção com o seguinte ID não existe: {pedido_id}")
        out = await alterar_tipo_estado_pedido_manutencao(db, pedido_id, estado_data.novo_estado_id)
        if out is False:
            return False, "Erro ao alterar o tipo de estado do pedido de manutenção com o ID {pedido_id}"
        if out is True:
            return True, "Tipo de estado alterado com sucesso"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException as es:
        raise es

@router.put("/manutencao/update{pedido_id}/estado")
async def atualizar_estado_manutencao(manutencao_id: int, estado_data: EstadoUpdate, db: Session = Depends(get_db)):
    try:
        obter = await obter_manutencao(db, manutencao_id)
        if obter is None:
            raise HTTPException(status_code=404, detail="Manutenção com o seguinte ID não existe: {pedido_id}")
        out = await alterar_tipo_estado_pedido_manutencao(db, manutencao_id, estado_data.novo_estado_id)
        if out is False:
            return False, "Erro ao alterar o tipo de estado da manutenção com o ID {pedido_id}"
        if out is True:
            return True, "Tipo de estado alterado com sucesso"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException as es:
        raise es

@router.put("/manutencao/update/")
async def atualizar_manutencao(manutencao: ManutencaoUpdateSchema, db: Session = Depends(get_db)):
    try:
        val, msg = await update_manutencao(db, manutencao)
        if val is False:
            return False, msg
        if val is True:
            return True, "Manutenção atualizada com sucesso"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/pedidosmanutencao/update/")
async def atualizar_pedido_manutencao(manutencao: PedidoManutencaoUpdateSchema, db: Session = Depends(get_db)):
    try:
        val, msg = await (
            update_pedido_manutencao(db, manutencao))
        if val is False:
            return False, msg
        if val is True:
            return True, "Pedido de manutenção atualizada com sucesso"
        if val is None:
            raise HTTPException(status_code=500)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))