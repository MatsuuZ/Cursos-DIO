from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas

def criar_atleta(db: Session, atleta: schemas.AtletaBase):
    novo_atleta = models.Atleta(**atleta.dict())
    try:
        db.add(novo_atleta)
        db.commit()
        db.refresh(novo_atleta)
        return novo_atleta
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um atleta cadastrado com o CPF: {atleta.cpf}"
        )

def listar_atletas(db: Session, nome: str = None, cpf: str = None):
    query = db.query(models.Atleta)
    if nome:
        query = query.filter(models.Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter(models.Atleta.cpf == cpf)
    return query.all()
