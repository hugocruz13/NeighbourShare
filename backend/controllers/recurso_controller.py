from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException
from middleware.auth_middleware import *
from db.session import get_db
from db.repository.recurso_repo import delete_recurso_db, existe_recurso
from sqlalchemy.orm import Session
from schemas.recurso_schema import *
from typing import List
import decimal
from services.recurso_service import *
from middleware.auth_middleware import role_required
from schemas.user_schemas import UserJWT

router = APIRouter(prefix="/recursos", tags=["Recursos"])

@router.post("/inserir")
async def inserir_recurso(
        token : UserJWT = Depends(role_required(["admin", "gestor","residente"])),
        nome_recurso: str = Form(...),
        descricao_recurso: str = Form(...),
        caucao_recurso: decimal.Decimal = Form(...),
        recurso_disponivel: str = Form(...),
        categoria_recurso: str = Form(...),
        fotos_recurso: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    try:
        recurso_data = RecursoInserirSchema(Nome=nome_recurso,
        DescRecurso= descricao_recurso,
        Caucao= caucao_recurso,
        CatID= await get_categoria_id_service(db, categoria_recurso),
        DispID = await get_disponibilidade_id_service(db, recurso_disponivel),
        UtilizadorID = token.id)

        sucesso, msg = await inserir_recurso_service(db, recurso_data, fotos_recurso)

        if sucesso:
            return {"message": "Recurso inserido com sucesso"}
        else:
            raise HTTPException(status_code=400, detail=msg)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Lista todos os recursos registados
@router.get("/", response_model=List[RecursoGetTodosSchema])
async def listar_recursos(
        db:Session = Depends(get_db),
        token: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))):
    """
    Endpoint para consultar todos os recursos
    """
    try:
        return await lista_recursos_service(db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categorias")
async def listar_categorias(
        token: UserJWT = Depends(role_required(["admin", "gestor", "residente"])),
        db: Session = Depends(get_db)
):
    try:
        return await lista_categorias_service(db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/disponibilidades")
async def listar_disponibilidades(
        token: UserJWT = Depends(role_required(["admin", "gestor", "residente"])),
        db: Session = Depends(get_db)
):
    try:
        return await lista_disponibilidades_service(db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Lista os recursos de um utilizador
@router.get("/pessoais", response_model=List[RecursoGetUtilizadorSchema])
async def listar_recursos_pessoais(
        token: UserJWT = Depends(role_required(["admin","gestor","residente"])),
        db:Session = Depends(get_db)):
    try:
        return await lista_recursos_utilizador_service(db, token.id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{recurso_id}", response_model=RecursoGetTodosSchema)
async def listar_recurso( recurso_id: int, token: UserJWT = Depends(role_required(["admin","gestor","residente"])),db:Session = Depends(get_db)):
    try:
        return await lista_recurso_service(db, recurso_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

##Update a info de um recurso
@router.put("/update")
async def update_recurso(
    id: int = Form(...),
    nome: Optional[str] = Form(None),
    descricao: Optional[str] = Form(None),
    caucao: Optional[decimal.Decimal] = Form(None),
    disponivel: Optional[str] = Form(None),
    categoria: Optional[str] = Form(None),
    foto: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user: UserJWT = Depends(role_required(["admin", "residente", "gestor"]))
):
    try:
        cat = await get_categoria_id_service(db, categoria) if categoria is not None else None
        disp = await get_disponibilidade_id_service(db, disponivel) if disponivel is not None else None
        recurso = UpdateRecursoSchema(Id=id, Nome=nome, DescRecurso=descricao, Caucao=caucao, CatId=cat, DispId=disp)

        if await update_service(db, recurso, foto):
            return {"message": "Dados atualizados com sucesso."}
        else:
            return {"message": "Erro ao atualizar os dados."}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{recurso_id}")
async def delete_recurso(recurso_id: int, token: UserJWT = Depends(role_required(["admin","gestor","residente"])),db:Session = Depends(get_db)):
    try:
        if await existe_recurso(db, recurso_id):
            if await delete_recurso_db(db, recurso_id):
                return {"message": "Recurso deletado com sucesso"}
            else:
                raise HTTPException(status_code=500, detail="Erro ao apagar o recurso.")
        else:
            raise HTTPException(status_code=404, detail="Recurso não existe.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


