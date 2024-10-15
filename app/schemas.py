from datetime import datetime

from pydantic import BaseModel
from pydantic import Field
from pydantic import PositiveFloat
from pydantic import EmailStr
from pydantic import field_validator

from typing import Annotated
from typing import Optional
from typing import List
import re

class ProductImageCreate(BaseModel):
    image_url: str
    is_main: bool = False
    order: Optional[int] = 0

class ProductImage(BaseModel):
    pk_id: int
    product_id: int
    image_url: str
    is_main: bool
    order: int
    created_at: datetime

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
    discount_price: Optional[float] = None
    barcode: Optional[str] = None
    is_active: bool = True

class ProductCreate(ProductBase):
    category_id: int
    images: List[ProductImageCreate] = []

class Product(ProductBase):
    pk_id: int
    category_id: int
    created_at: datetime
    updated_at: datetime
    images: List[ProductImage]

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    slug: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    pk_id: int
    products: List[Product]

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    surname: str
    user_name: str
    email: EmailStr  # O pydantic já tem validação embutida para emails
    phone_number: Optional[str] = None

    @field_validator('phone_number')
    def validate_phone(cls, phone_number):
        phone_regex = r'^\+\d{1,3}\s\d{1,4}[-\s]\d{4,5}[-\s]?\d{4}$'
        if phone_number and not re.match(phone_regex, phone_number):
            raise ValueError('O número de telefone não é válido. O formato correto é: +55 92 99999-9999')
        return phone_number

class UserCreate(UserBase):
    password: str  # Adicionar a senha ao criar o usuário

class User(UserBase):
    pk_id: int
    is_active: bool

    class Config:
        from_attributes = True

# Esquemas para Order
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    pk_id: int
    total: float

    class Config:
        from_attributes = True

class ShippingAddressBase(BaseModel):
    address: str
    city: str
    state: str
    postal_code: str
    country: str

class ShippingAddressCreate(ShippingAddressBase):
    pass

class ShippingAddress(ShippingAddressBase):
    pk_id: int

    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    payment_method: str
    payment_status: Optional[str] = "Pending"
    amount: float

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    pk_id: int
    payment_date: datetime

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    user_id: int
    total_price: float
    shipping_cost: Optional[float] = 0
    status: Optional[str] = "Pending"

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]
    shipping_address: ShippingAddressCreate
    payment: PaymentCreate

class Order(OrderBase):
    pk_id: int
    created_at: datetime
    updated_at: datetime
    items: List[OrderItem]
    payment: Payment
    shipping_address: ShippingAddress

    class Config:
        from_attributes = True