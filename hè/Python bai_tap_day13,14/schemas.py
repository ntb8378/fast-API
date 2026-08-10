from pydantic import BaseModel, Field
from typing import Optional, List

class  ProductCreate(BaseModel):
    product_code : str = Field(...,min_length=4 , max_length= 10)
    name : str = Field(...,min_length=2 , max_length= 100)
    price : float = Field(...,gt=0)
    stock_quantity : int = Field(...,gt=0)
    category_id : int = Field(...)

class ProductUpdate(BaseModel):
    price : Optional[float] = Field(None,gt = 0)
    stock_quantity : Optional[int] = Field(None,ge = 0)

class OrderItemCreate(BaseModel):
    product_id : int = Field(...)
    quantity : int = Field(gt= 0)

class OrderCreate(BaseModel):
    customer_name : str = Field(...)
    items : List[OrderItemCreate]

class ProductResponse(BaseModel):
    id : int
    product_code : str
    name : str 
    price : float 
    stock_quantity : int 

    class Config():
        from_attribute = True

class OrderResponse(BaseModel):
    id: int
    order_code : str
    customer_name : str
    total_amount : float
    status : str

    class Config():
            from_attribute = True