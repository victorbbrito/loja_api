from sqlalchemy.orm import Session
import models
import schemas
from datetime import datetime

def get_products(db:Session):
    return db.query(models.Product).all()

def get_product_by_id(db:Session, product_id: int):
    return db.query(models.Product).filter(models.Product.pk_id == product_id).first()

def get_products_by_category(db: Session, category: str):
    return db.query(models.Product).filter(models.Product.category.like(f"%{category}%")).all()

def get_products_by_name(db:Session, name: str):
    return db.query(models.Product).filter(models.Product.name.like(f"%{name}%")).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product:schemas.ProductOutput = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_data: schemas.ProductUpdate):
    
    db_product = db.query(models.Product).filter(models.Product.pk_id == product_id).first()
    
    if db_product is None:
        db.rollback()
        return None

    for key, value in product_data.model_dump(exclude_unset=True).items():
        setattr(db_product, key, value)
        setattr(db_product, "updated_at", datetime.now())

    db.commit()
    db.refresh(db_product)

    return db_product
