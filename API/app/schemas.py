from pydantic import BaseModel
from typing import Optional

class CategoriaBase(BaseModel):
    nome: str

class CategoriaResponse(CategoriaBase):
    pk_id: int
    class Config:
        orm_mode = True

class CentroTreinamentoBase(BaseModel):
    nome: str
    endereco: Optional[str]
    proprietario: Optional[str]

class CentroTreinamentoResponse(CentroTreinamentoBase):
    pk_id: int
    class Config:
        orm_mode = True

class AtletaBase(BaseModel):
    nome: str
    cpf: str
    idade: Optional[int]
    peso: Optional[float]
    altura: Optional[float]
    sexo: Optional[str]
    centro_treinamento_id: int
    categoria_id: int

class AtletaResponse(AtletaBase):
    pk_id: int
    centro_treinamento: CentroTreinamentoResponse
    categoria: CategoriaResponse
    class Config:
        orm_mode = True
