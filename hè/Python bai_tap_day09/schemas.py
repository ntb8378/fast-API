from pydantic import BaseModel
from typing import Optional

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    price: Optional[float]
    quantity: Optional[int]