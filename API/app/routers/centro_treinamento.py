from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database
from fastapi_pagination import Page, paginate

router = APIRouter()

@router.post("/", response_model=schemas.CentroTreinamentoResponse)
def criar_centro(centro: schemas.CentroTreinamentoBase, db: Session = Depends(database.get_db)):
    novo_centro = models.CentroTreinamento(**centro.dict())
    db.add(novo_centro)
    db.commit()
    db.refresh(novo_centro)
    return novo_centro

@router.get("/", response_model=Page[schemas.CentroTreinamentoResponse])
def listar_centros(db: Session = Depends(database.get_db)):
    centros = db.query(models.CentroTreinamento).all()
    return paginate(centros)
