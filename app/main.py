from fastapi import FastAPI
import routers as product_router
from database import engine
import models

# Criar as tabelas no banco
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Store API")

# Inclui as rotas de produto
app.include_router(product_router.router)

@app.get("/")
def read_root():
    return {"mensagem": "Welcome to Store API",
            "developer":"Victor Brito"}