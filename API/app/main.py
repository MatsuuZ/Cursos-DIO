from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.routers import atleta, categoria, centro_treinamento

app = FastAPI(title="WorkoutAPI")

app.include_router(atleta.router, prefix="/atleta", tags=["Atleta"])
app.include_router(categoria.router, prefix="/categoria", tags=["Categoria"])
app.include_router(centro_treinamento.router, prefix="/centro", tags=["Centro de Treinamento"])

add_pagination(app)
