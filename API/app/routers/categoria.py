from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database
from fastapi_pagination import Page, paginate

router = APIRouter()

@router.post("/", response_model=schemas.CategoriaResponse)
def criar_categoria(categoria: schemas.CategoriaBase, db: Session = Depends(database.get_db)):
    nova_categoria = models.Categoria(**categoria.dict())
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    return nova_categoria

@router.get("/", response_model=Page[schemas.CategoriaResponse])
def listar_categorias(db: Session = Depends(database.get_db)):
    categorias = db.query(models.Categoria).all()
    return paginate(categorias)
