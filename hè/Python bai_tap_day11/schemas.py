from pydantic import BaseModel

class BookCreate(BaseModel):
    title : str
    author : str
    category : str
    price : float
    borrow_count : int = 0
    available_quantity : int = 0
    