from pydantic import BaseModel, ConfigDict

class BookCreate(BaseModel):
    title : str
    author_id : int
    category : str
    price : float
    borrow_count : int = 0
    available_quantity : int = 0

class AuthorResponseSchema(BaseModel):
    id: int
    name: str
    email: str


class BookResponseSchema(BookCreate):
    id: int
    author: AuthorResponseSchema

    model_config = ConfigDict(from_attributes=True)
