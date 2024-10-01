from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Column

from datetime import datetime

from database import Base

class Product(Base):
    __tablename__ = 'products' 

    pk_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    category = Column(String, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)
    quantity = Column(Integer)
    barcode = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    