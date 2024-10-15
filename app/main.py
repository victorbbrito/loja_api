from fastapi import FastAPI
from app.routers import router
from app.database import engine
import app.models as models

# Criar as tabelas no banco
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Store API")

# Inclui as rotas de produto
app.include_router(router)

@app.get("/")
def read_root():
    return {"mensagem": "Welcome to Store API",
            "developer":"Victor Brito"}