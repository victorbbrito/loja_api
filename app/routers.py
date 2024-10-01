from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from database import get_db

router = APIRouter()

@router.get("/products/", response_model=List[schemas.ProductOutput])
def get_all_products(db: Session = Depends(get_db)):
    return crud.get_products(db=db)

@router.get("/products/{product_id}", response_model=schemas.ProductOutput)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db=db, product_id=product_id)
    
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")
    
    return product

@router.get("/products/{product_name}", response_model=List[schemas.ProductOutput])
def get_products_by_name(product_name:str, db: Session = Depends(get_db)):
    products = crud.get_products_by_name(db=db, name= product_name)
    
    if products is []:
        raise HTTPException(status_code=404, detail="A product with the given name was not found.")
    
    return products

@router.get("/products/{product_category}", response_model=List[schemas.ProductOutput])
def get_products_by_category(product_category:str, db: Session = Depends(get_db)):
    products = crud.get_products_by_category(db=db, category= product_category)
    
    if products is []:
        raise HTTPException(status_code=404, detail="A product with the given category was not found.")
    
    return products

@router.patch("/products/{product_id}", response_model=schemas.ProductOutput)
def update_product_by_id(product_id:int, product_up: schemas.ProductUpdate, db:Session = Depends(get_db)):
    product = crud.update_product(db=db, product_id=product_id, product_data=product_up)
    
    if product is None:
        raise HTTPException(status_code=404, detail="A product with the given id was not found.")
    
    return product

@router.post("/products/", response_model=schemas.ProductOutput)
def create_new_product(product_in: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product_in)
