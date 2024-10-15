from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi import Security
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from typing import List

import app.crud as crud
import app.schemas as schemas
import app.auth as auth
from app.database import get_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Rota de login para obter o token JWT
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos.")
    access_token = auth.create_access_token(data={"sub": user.user_name})
    return {"access_token": access_token, "token_type": "bearer"}

# Rota de atualização do usuário
@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserBase, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = auth.verify_token(token)
    if not current_user or current_user["sub"] != user.user_name and not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Você não tem permissão para atualizar este usuário.")
    
    db_user = crud.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    # Atualizando as informações do usuário
    db_user.name = user.name
    db_user.surname = user.surname
    db_user.email = user.email
    db_user.phone_number = user.phone_number
    db.commit()
    db.refresh(db_user)
    return db_user

# Rota de atualização do produto
@router.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.Product, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = auth.verify_token(token)
    if not current_user:
        raise HTTPException(status_code=403, detail="Usuário não autenticado.")
    
    db_product = crud.get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    # Apenas o admin ou o criador do produto podem atualizá-lo
    if current_user.get("role") != "admin" and db_product.created_by != current_user["sub"]:
        raise HTTPException(status_code=403, detail="Você não tem permissão para atualizar este produto.")
    
    # Atualizando as informações do produto
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.discount_price = product.discount_price
    db_product.quantity = product.quantity
    db.commit()
    db.refresh(db_product)
    return db_product

# Função para verificar se o usuário é admin
def is_admin(user):
    return user.get("role") == "admin"

@router.post("/products/", summary="Create a new product", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@router.get("/products/", summary="Get all products" , response_model=List[schemas.Product])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_products(db, skip=skip, limit=limit)

@router.get("/products/{product_id}", summary="Get a product by id", response_model=schemas.Product)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/products/{product_id}", summary="Delete a product", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return crud.delete_product(db, product_id=product_id)

@router.get("/products/category/{category_id}", summary="Get all products by category id", response_model=List[schemas.Product])
def get_products_by_category(category_id:int ,db: Session = Depends(get_db)):
    return crud.get_products_by_category_id(db, category_id)

@router.get("/products/{name}", summary="Get all products where product name is the same as name",response_model=List[schemas.Product])
def get_products_by_name(name:str ,db: Session = Depends(get_db)):
    return crud.get_products_by_name(db, name)

# Rotas para Categorias
@router.post("/categories/", summary="Create a new category", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db=db, category=category)

@router.get("/categories/", summary="Get all categories", response_model=List[schemas.Category])
def get_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_categories(db, skip=skip, limit=limit)

@router.post("/users/", summary="Create new user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    return crud.create_user(db=db, user=user)

@router.get("/users/", summary="Get all users", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@router.get("/users/{user_id}", summary="Get a user by id",response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return db_user

@router.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db=db, order=order)

@router.get("/orders/", response_model=List[schemas.Order])
def get_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip=skip, limit=limit)

@router.get("/orders/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order_by_id(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order