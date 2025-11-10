from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Categoria(Base):
    __tablename__ = "categoria"
    pk_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(10), unique=True, nullable=False)
    atletas = relationship("Atleta", back_populates="categoria")

class CentroTreinamento(Base):
    __tablename__ = "centro_treinamento"
    pk_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(20), unique=True, nullable=False)
    endereco = Column(String(60))
    proprietario = Column(String(30))
    atletas = relationship("Atleta", back_populates="centro_treinamento")

class Atleta(Base):
    __tablename__ = "atleta"
    pk_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    idade = Column(Integer)
    peso = Column(Float)
    altura = Column(Float)
    sexo = Column(String(1))
    centro_treinamento_id = Column(Integer, ForeignKey("centro_treinamento.pk_id"))
    categoria_id = Column(Integer, ForeignKey("categoria.pk_id"))

    centro_treinamento = relationship("CentroTreinamento", back_populates="atletas")
    categoria = relationship("Categoria", back_populates="atletas")
