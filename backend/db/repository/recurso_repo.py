from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.orm import joinedload
from db import session
from db.models import Recurso, Disponibilidade, Categoria, Reserva, PedidoReserva
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from schemas.reserva_schema import PedidoReservaEstadosSchema
from schemas.recurso_schema import DisponibilidadeEstadosSchema

def get_disponibilidade_id_db(disponibilidade:str, db:session):
    try:
            disponibilidade_id = db.query(Disponibilidade).filter(Disponibilidade.DescDisponibilidade == disponibilidade).first().DispID
            if disponibilidade_id:
                return disponibilidade_id
            else:
                raise Exception("Nenhuma disponibilidade encontrada com o nome informado")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_categoria_id_db(categoria:str, db:session):
    try:
        categoria_id = db.query(Categoria).filter(Categoria.DescCategoria == categoria).first().CatID
        if categoria_id:
            return categoria_id
        else:
            raise Exception("Nenhuma categoria encontrada com o nome informado")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def inserir_recurso_db(db:session, recurso:Recurso):
    try:
        novo_recurso = Recurso(
            Nome=recurso.Nome,
            DescRecurso=recurso.DescRecurso,
            Caucao=recurso.Caucao,
            UtilizadorID=recurso.UtilizadorID,
            DispID = recurso.DispID,
            CatID=recurso.CatID,
            Path="none"
        )
        db.add(novo_recurso)
        db.commit()
        db.refresh(novo_recurso)

        return novo_recurso.RecursoID, {'Inserção do recurso realizada com sucesso!'}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def update_path(db: session, id: int, path: str):
    try:
        db.query(Recurso).filter(Recurso.RecursoID == id).update({Recurso.Path: path})
        db.commit()
        return {"message": "Caminho da imagem atualizado com sucesso."}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

#Lista todos os recursos registados no sistema
async def listar_recursos_db(db:session):
    try:
        recursos = (
            db.query(Recurso)
            .options(
                joinedload(Recurso.Utilizador_),
                joinedload(Recurso.Categoria_),
                joinedload(Recurso.Disponibilidade_)
            )
            .all()
        )
        return recursos
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

#Lista as informações referentes a um recurso registado no sistema
async def listar_recurso_db(db:session, recurso_id:int):
    try:
        recurso = db.query(Recurso).filter(Recurso.RecursoID == recurso_id).first()
        return recurso
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

#Lista os recursos pertencentes a um utilizador (utilizador_id)
async def listar_recursos_utilizador_db(db:session, utilizador_id:int):
    try:
        recursos = (
            db.query(Recurso)
            .filter(Recurso.UtilizadorID == utilizador_id)
            .options(
                joinedload(Recurso.Utilizador_),
                joinedload(Recurso.Categoria_),
                joinedload(Recurso.Disponibilidade_)
            )
            .all()
        )
        return recursos
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

#Função para atualizar o estado de todos os recursos tendo em conta se está reservado ou não
async def atualizar_disponibilidade_recurso_db(db:session):
    try:
        hoje = date.today()

        recursos = db.query(Recurso).all()

        for recurso in recursos:
            reserva_ativa = (
                db.query(Reserva)
                .join(PedidoReserva, PedidoReserva.RecursoID == Recurso.RecursoID)
                .filter(
                    PedidoReserva.RecursoID == Recurso.RecursoID,
                    PedidoReserva.DataInicio <= hoje,
                    PedidoReserva.DataFim >= hoje,
                    PedidoReserva.EstadoPedidoReserva_.DescEstadoPedidoReserva == PedidoReservaEstadosSchema.APROVADO
                )
                .first()
            )

            recurso.DispID = DisponibilidadeEstadosSchema.INDISPONIVEL if reserva_ativa else DisponibilidadeEstadosSchema.DISPONIVEL

        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
#Função que muda a disponibilidade de um recurso para indisponivel
async def muda_recurso_para_indisponivel_db(db:session, recurso_id:int):
    try:
        recurso = db.query(Recurso).filter(Recurso.RecursoID == recurso_id).first()
        recurso.DispID = DisponibilidadeEstadosSchema.INDISPONIVEL
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def existe_recurso(db:session, recurso_id:int):
    try:
        recurso = db.query(Recurso).filter(Recurso.RecursoID == recurso_id).first()
        return recurso
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))