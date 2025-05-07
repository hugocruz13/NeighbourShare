from fastapi import APIRouter, File, Form
from db.session import get_db
from services.recurso_comum_service import *
from middleware.auth_middleware import *
from schemas.user_schemas import UserJWT

router = APIRouter(prefix="/recursoscomuns", tags=["Recursos Comuns"])

#region Pedidos de Manutenção de Recursos Comuns

#Inserção de um pedido de manutenção de um recurso comum
@router.post("/pedidosmanutencao/inserir")
async def inserir_manutencao_recurso_comum(
    pedido: PedidoManutencaoRequest,
    token: UserJWT = Depends(role_required(["admin","gestor", "residente"])),
    db:Session = Depends(get_db)
):
    novo_pedido_manutencao = PedidoManutencaoSchemaCreate(
        UtilizadorID=token.id,
        RecComumID=pedido.recurso_comum_id,
        DescPedido=pedido.desc_manutencao_recurso_comum,
        DataPedido = date.today(),
        EstadoPedManuID= 1 # Relativo ao estado 'Em análise'
    )

    return await inserir_pedido_manutencao_service(db, novo_pedido_manutencao)

#Listar os pedidos de manutenção existentes no sistema
@router.get("/pedidosmanutencao")
async def listar_pedidos_manutencao(db:Session = Depends(get_db), token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))
):
    """
    Endpoint para consultar todos os pedidos de manutenção de recursos comuns
    """
    return await listar_pedidos_manutencao_service(db)

#Endpoint para eliminar um pedido de manutenção
@router.delete("/pedidosmanutencao/eliminar/{pedido_id}")
async def eliminar_pedido_manutencao(
        pedido_id:int,
        db:Session = Depends(get_db),
        token: UserJWT = Depends(role_required(["admin", "gestor"]))
):
    try:
        return await eliminar_pedido_manutencao_service(db, pedido_id, token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pedidosmanutencao/estados")
async def listar_tipos_pedido_manutencao(db:Session = Depends(get_db), token: UserJWT=Depends(role_required(["admin", "residente", "gestor"]))):
    return await obter_all_tipo_estado_pedido_manutencao(db)

@router.put("/pedidosmanutencao/{pedido_id}/estado")
async def atualizar_estado_pedido(pedido_id: int, estado_data: EstadoUpdate, token: UserJWT=Depends(role_required(["admin","gestor"])),db: Session = Depends(get_db)):
    try:
        obter = await obter_pedido_manutencao(db, pedido_id)
        if obter is None:
            raise HTTPException(status_code=404, detail="Pedido de manutenção com o seguinte ID não existe: {pedido_id}")
        out = await alterar_tipo_estado_pedido_manutencao(db, pedido_id, estado_data.novo_estado_id.value)
        if out is False:
            return False, "Erro ao alterar o tipo de estado do pedido de manutenção com o ID {pedido_id}"
        return True, "Tipo de estado alterado com sucesso"
    except HTTPException as es:
        raise es
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/pedidosmanutencao/update/")
async def atualizar_pedido_manutencao(manutencao: PedidoManutencaoUpdateSchema, db: Session = Depends(get_db), token: UserJWT = Depends(role_required(["admin", "gestor"]))):
    try:
        val, msg = await (
            update_pedido_manutencao(db, manutencao, token))
        if val is False:
            return False, msg
        if val is True:
            return True, "Pedido de manutenção atualizada com sucesso"
        if val is None:
            raise HTTPException(status_code=500)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#endregion

#region Manutenção de Recursos Comuns
@router.post("/manutencao/inserir")
async def inserir_manutencao(manutencao:ManutencaoCreateSchema,db:Session = Depends(get_db), token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))):
    try:
        return await criar_manutencao_service(db,manutencao);
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/manutencao/")
async def listar_manutencoes(db:Session = Depends(get_db), token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))):
    return await visualizar_manutencoes(db)

@router.get("/manutencao/estados")
async def listar_tipos_manutencao(db: Session = Depends(get_db), token:UserJWT=Depends(role_required(["admin", "residente", "gestor"]))):
    return await obter_all_tipo_estado_manutencao(db)

@router.put("/manutencao/update/{manutencao_id}/estado")
async def atualizar_estado_manutencao(manutencao_id: int, estado_data: EstadoUpdate, token:UserJWT=Depends(role_required(["admin","gestor"])),db: Session = Depends(get_db)):
    try:
        obter = await obter_manutencao(db, manutencao_id)
        if obter is None:
            raise HTTPException(status_code=404, detail="Manutenção com o seguinte ID não existe: {pedido_id}")
        out = await alterar_tipo_estado_manutencao(db, manutencao_id, estado_data.novo_estado_id.value)
        if out is False:
            return False, "Erro ao alterar o tipo de estado da manutenção com o ID {pedido_id}"
        if out is True:
            return True, "Tipo de estado alterado com sucesso"
    except HTTPException as es:
        raise es
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/manutencao/update/")
async def atualizar_manutencao(manutencao: ManutencaoUpdateSchema, db: Session = Depends(get_db),token: UserJWT = Depends(role_required(["admin", "gestor"]))):
    try:
        return await update_manutencao(db, manutencao)
    except HTTPException as es:
        raise es
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/manutencao/eliminar/{manutencao_id}")
async def eliminar_manutencao(manutencao_id: int, db:Session = Depends(get_db), token: UserJWT = Depends(role_required(["admin", "gestor"]))):
    try:
        return await eliminar_manutencao_service(db, manutencao_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#endregion

#region Gestão Recursos Comuns

#Inserção de um novo recurso comum
@router.post("/inserir")
async def inserir_recurso_comum(
        nome_recurso:str = Form(...),
        descricao_recurso:str = Form(...),
        imagem : UploadFile = File(...),
        db:Session = Depends(get_db),
        token: UserJWT = Depends(role_required(["admin","gestor"]))):
   try:
       novo_recurso_comum = RecursoComumSchemaCreate(Nome=nome_recurso, DescRecursoComum=descricao_recurso)
       return await inserir_recurso_comum_service(db, novo_recurso_comum, imagem)
   except Exception as e:
       raise RuntimeError(f"Erro atualizar novo utilizador: {e}")

#Inserção de um pedido de um novo recurso comum
@router.post("/pedidosnovos/inserir")
async def inserir_pedido_novo_recurso_comum(
    desc_pedido_novo_recurso: str,
    db:Session = Depends(get_db),
    token: UserJWT = Depends(role_required(["admin","gestor", "residente"]))
):
    novo_pedido = PedidoNovoRecursoSchemaCreate(
        DescPedidoNovoRecurso=desc_pedido_novo_recurso,
        UtilizadorID=token.id,
        DataPedido = date.today(),
        EstadoPedNovoRecID= 1 # Referente ao estado 'Pendente'
    )

    return await inserir_pedido_novo_recurso_service(db,novo_pedido)

@router.get("/pedidosnovos")
async def listar_pedidos_novos_recursos(db:Session = Depends(get_db),token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))):
    """
    Endpoint para consultar todos os pedidos de novos recursos comuns
    """
    return await listar_pedidos_novos_recursos_service(db)

@router.get("/")
async def get_recurso_comum(db:Session = Depends(get_db),token: UserJWT = Depends(role_required(["admin","gestor", "residente"]))):
    try:
        return await get_recursos_comuns(db)
    except Exception as e:
        raise RuntimeError(f"Erro atualizar novo utilizador: {e}")

@router.get("/{recurso_id}")
async def get_recurso_comum_by_id(recurso_id: int,db:Session = Depends(get_db),token: UserJWT = Depends(role_required(["admin","gestor", "residente"]))):
    try:
        return await get_recursos_comuns_by_id(db,recurso_id)
    except Exception as e:
        raise RuntimeError(f"Erro atualizar novo utilizador: {e}")

#endregion