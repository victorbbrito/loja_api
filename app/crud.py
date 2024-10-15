from datetime import datetime
from sqlalchemy.orm import Session
from app import models, schemas

# Adicionar um novo produto
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        discount_price=product.discount_price,
        quantity=product.quantity,
        barcode=product.barcode,
        category_id=product.category_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # Adicionando imagens ao produto
    for image in product.images:
        db_image = models.ProductImage(
            product_id=db_product.pk_id,
            image_url=image.image_url,
            is_main=image.is_main,
            order=image.order
        )
        db.add(db_image)
    
    db.commit()
    return db_product

# Buscando todos os produtos
def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()

# Buscando um produto pelo id
def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.pk_id == product_id).first()

# Buscando todos os produtos pela categoria
def get_products_by_category_id(db: Session, category_id: int):
    return db.query(models.Product).filter(models.Product.category_id == category_id).all()

# Buscando produtos pelo nome
def get_products_by_name(db: Session, product_name: str):
    return db.query(models.Product).filter(models.Product.name.like(f"%{product_name}%")).all()

# Atualizando as informaçoes de um produto
def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_product = get_product_by_id(db, product_id)
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.discount_price = product.discount_price
        db_product.quantity = product.quantity
        db_product.barcode = product.barcode
        db_product.is_active = product.is_active
        db_product.updated_at = datetime.now()

        db.commit()
        db.refresh(db_product)
    return db_product

# Deletando um produto
def delete_product(db: Session, product_id: int):
    db_product = get_product_by_id(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

# ______________________________________________________________________________________

# CRUD Categoria
def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(
        name=category.name,
        slug=category.slug
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_category_by_id(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.pk_id == category_id).first()

# ___________________________________________________________________________________________________

# CRUD Usuário
def create_user(db: Session, user: schemas.UserCreate):
    # Validando o email e telefone
    models.User.validate_email(user.email)
    models.User.validate_phone_number(user.phone_number)
    
    db_user = models.User(
        name=user.name,
        surname=user.surname,
        user_name=user.user_name,
        email=user.email,
        phone_number=user.phone_number,
    )
    db_user.set_password(user.password)  # Criptografar a senha
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Buscar todos os usuários
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

# Buscar usuário por ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.pk_id == user_id).first()

# Buscar usuário pelo user_name
def get_user_by_user_name(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.user_name == user_name).first()

# Buscar usuário por email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def update_user(db: Session, user_id: int, user: schemas.User):
    
    try:
        models.User.validate_email(user.email)
        models.User.validate_phone_number(user.phone_number)
    
    except Exception as error:
        return error
    
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db_user.is_active = user.is_active
        db_user.email = user.email
        db_user.phone_number = user.phone_number
        db_user.updated_at = datetime.now()

        db.commit()
        db.refresh(db_user)
    return db_user

def update_user_password(db: Session, user_name: str, user: schemas.UserCreate):
    db_user = get_user_by_user_name(db, user_name)
    if db_user:
        db_user.set_password(user.password)

        db.commit()
        db.refresh()
    return db_user
# __________________________________________________________________________________________

# CRUD Vendas
def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(
        user_id=order.user_id,
        total_price=order.total_price,
        shipping_cost=order.shipping_cost
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Adicionando os itens à venda
    for item in order.items:
        db_item = models.OrderItem(
            order_id=db_order.pk_id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price,
            total=item.price * item.quantity
        )
        db.add(db_item)
    
    # Adicionando o endereço de entrega
    db_shipping_address = models.ShippingAddress(
        order_id=db_order.pk_id,
        address=order.shipping_address.address,
        city=order.shipping_address.city,
        state=order.shipping_address.state,
        postal_code=order.shipping_address.postal_code,
        country=order.shipping_address.country
    )
    db.add(db_shipping_address)

    # Adicionando o pagamento
    db_payment = models.Payment(
        order_id=db_order.pk_id,
        payment_method=order.payment.payment_method,
        payment_status=order.payment.payment_status,
        amount=order.payment.amount
    )
    db.add(db_payment)

    db.commit()
    return db_order

# Buscar todas as vendas
def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Order).offset(skip).limit(limit).all()

# Buscar uma venda por ID
def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.pk_id == order_id).first()