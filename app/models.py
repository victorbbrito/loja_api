from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy.orm import relationship
import bcrypt
import re

from datetime import datetime

from app.database import Base

class Product(Base):
    __tablename__ = 'products'

    pk_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    
    category_id = Column(Integer, ForeignKey('categories.pk_id'), nullable=False)
    category = relationship('Category', back_populates='products')
    
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    discount_price = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    
    barcode = Column(String, nullable=True)
    slug = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    # Relacionamento com a tabela de imagens
    images = relationship('ProductImage', back_populates='product', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product(name='{self.name}', price='{self.price}', quantity='{self.quantity}', category='{self.category.name}')>"

class ProductImage(Base):
    __tablename__ = 'product_images'

    pk_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    
    # Chave estrangeira referenciando o produto
    product_id = Column(Integer, ForeignKey('products.pk_id'), nullable=False)
    product = relationship('Product', back_populates='images')
    
    image_url = Column(String, nullable=False)  # URL ou caminho da imagem
    
    # Campo para definir a ordem de exibição ou se é a imagem principal
    is_main = Column(Boolean, default=False)  # Define se é a imagem principal
    order = Column(Integer, default=0)  # Ordenação das imagens
    
    created_at = Column(DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f"<ProductImage(product_id='{self.product_id}', image_url='{self.image_url}', is_main='{self.is_main}')>"

# Exemplo de uma tabela de categorias
class Category(Base):
    __tablename__ = 'categories'

    pk_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    slug = Column(String, nullable=False, unique=True)
    
    products = relationship('Product', back_populates='category')

    def __repr__(self):
        return f"<Category(name='{self.name}')>"

class PasswordTooWeakError(Exception):
    """Exceção personalizada para senhas fracas."""
    pass

class User(Base):
    __tablename__ = 'users'

    pk_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    user_name = Column(String(50), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    phone_number = Column(String(20), nullable=True, unique=True)  # Número de telefone com regex
    password = Column(String(255), nullable=False)
    image_profile = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    # Método para definir a senha e criptografar
    def set_password(self, password):
        self.validate_password_strength(password)  # Valida a força da senha antes de criptografar
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')  # Armazene como string

    # Método para verificar a senha na autenticação
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))  # Converta self.password para bytes

    # Valida a força da senha
    def validate_password_strength(self, password):
        if len(password) < 8:
            raise PasswordTooWeakError("A senha deve ter pelo menos 8 caracteres.")
        
        if not re.search(r'[A-Z]', password):
            raise PasswordTooWeakError("A senha deve conter pelo menos uma letra maiúscula.")
        
        if not re.search(r'[a-z]', password):
            raise PasswordTooWeakError("A senha deve conter pelo menos uma letra minúscula.")
        
        if not re.search(r'[0-9]', password):
            raise PasswordTooWeakError("A senha deve conter pelo menos um número.")
        
        if not re.search(r'[@$!%*#?&]', password):
            raise PasswordTooWeakError("A senha deve conter pelo menos um caractere especial (@, $, !, %, *, #, ?, &).")
        
        if re.search(r'\s', password):
            raise PasswordTooWeakError("A senha não pode conter espaços em branco.")
    
        if self.user_name.lower() in password.lower():
            raise PasswordTooWeakError("A senha não pode conter o nome de usuário.")

    # Validação do formato de email
    @staticmethod
    def validate_email(email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValueError("O email fornecido não é válido.")

    # Validação do formato do número de telefone
    @staticmethod
    def validate_phone_number(phone_number):
        phone_regex = r'^\+\d{1,3}\s\d{1,4}[-\s]\d{4,5}[-\s]?\d{4}$'  # Exemplo: +55 92 99999-9999
        if phone_number and not re.match(phone_regex, phone_number):
            raise ValueError("O número de telefone fornecido não é válido.")

    def __repr__(self):
        return f"<User(user_name='{self.user_name}', name='{self.name}', surname='{self.surname}', email='{self.email}')>"
    
class Order(Base):
    __tablename__ = 'orders'

    pk_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.pk_id'), nullable=False)
    user = relationship('User')  # Relacionamento com o usuário logado que fez a compra
    total_price = Column(Float, nullable=False)
    shipping_cost = Column(Float, nullable=True, default=0)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    status = Column(String(50), nullable=False, default="Pending")  # Status da compra (e.g., "Pending", "Shipped", "Delivered")

    items = relationship('OrderItem', back_populates='order', cascade="all, delete-orphan")
    payment = relationship('Payment', uselist=False, back_populates='order', cascade="all, delete-orphan")
    shipping_address = relationship('ShippingAddress', uselist=False, back_populates='order', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order(id='{self.pk_id}', user_id='{self.user_id}', total_price='{self.total_price}')>"

class OrderItem(Base):
    __tablename__ = 'order_items'

    pk_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.pk_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.pk_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

    order = relationship('Order', back_populates='items')
    product = relationship('Product')

    def __repr__(self):
        return f"<OrderItem(order_id='{self.order_id}', product_id='{self.product_id}', quantity='{self.quantity}')>"

class Payment(Base):
    __tablename__ = 'payments'

    pk_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.pk_id'), nullable=False)
    payment_method = Column(String(50), nullable=False)  # Meio de pagamento (e.g., "Credit Card", "PayPal")
    payment_status = Column(String(50), nullable=False, default="Pending")  # Status do pagamento (e.g., "Pending", "Paid")
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.now)

    order = relationship('Order', back_populates='payment')

    def __repr__(self):
        return f"<Payment(order_id='{self.order_id}', method='{self.payment_method}', status='{self.payment_status}')>"

class ShippingAddress(Base):
    __tablename__ = 'shipping_addresses'

    pk_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.pk_id'), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)

    order = relationship('Order', back_populates='shipping_address')

    def __repr__(self):
        return f"<ShippingAddress(order_id='{self.order_id}', address='{self.address}', city='{self.city}')>"