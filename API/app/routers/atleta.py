from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, database
from fastapi_pagination import Page, paginate

router = APIRouter()

@router.post("/", response_model=schemas.AtletaResponse)
def criar_atleta(atleta: schemas.AtletaBase, db: Session = Depends(database.get_db)):
    return crud.criar_atleta(db, atleta)

@router.get("/", response_model=Page[schemas.AtletaResponse])
def listar_atletas(nome: str = None, cpf: str = None, db: Session = Depends(database.get_db)):
    atletas = crud.listar_atletas(db, nome, cpf)
    return paginate(atletas)
