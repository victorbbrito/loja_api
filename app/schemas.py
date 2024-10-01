from pydantic import BaseModel
from pydantic import Field
from pydantic import PositiveFloat
from datetime import datetime
from typing import Annotated
from typing import Optional

class BaseSchema(BaseModel):
    
    class Config:
        extra = 'forbid'
        from_attributes = True
        
class BaseOutput(BaseSchema):
    pk_id: Annotated[int, Field(description="Identifier", example=1)]
    created_at: Annotated[datetime, Field(description="Created date")]
    updated_at: Annotated[datetime, Field(description="Updated date")]

class Product(BaseSchema):
    category: Annotated[str, Field(description="Product category", example="Games")]
    name: Annotated[str, Field(description="Product name", example="Good Of War Ragnarok")]
    price: Annotated[PositiveFloat, Field(description="Product price", example=199.99)]
    sell_price: Annotated[PositiveFloat, Field(description="Product sell price", example=279.99)]
    quantity: Annotated[int, Field(description="Product quantity in stock", example=20)]
    barcode: Annotated[str, Field(description="Product code", example="BR12024G4M3")]
    
class ProductCreate(Product):
    super

class ProductOutput(Product,BaseOutput):
    super
    
class ProductUpdate(BaseSchema):
    category: Annotated[Optional[str], Field(None,description="Product category", example="Games")]
    name: Annotated[Optional[str], Field(None,description="Product name", example="Good Of War Ragnarok")]
    price: Annotated[Optional[PositiveFloat], Field(None, description="Product price", example=199.99)]
    sell_price: Annotated[Optional[PositiveFloat], Field(None, description="Product sell price", example=279.99)]
    quantity: Annotated[Optional[int], Field(None, description="Product quantity in stock", example=20)]
    barcode: Annotated[Optional[str], Field(None, description="Product code", example="BR12024G4M3")]
    
    
