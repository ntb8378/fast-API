from fastapi import FastAPI,Depends
from database import Base, engine, get_db
from models import BookModel
from sqlalchemy.orm import Session
import Book_service
from schemas import BookCreate, BookResponse


app = FastAPI()

Base.metadata.create_all(bind= engine)

@app.get("/")
def test():
    return{
        "message": "kết nối thành công"
    }

@app.get("/books", response_model=list[BookResponse])
def get_book(db:Session = Depends(get_db)):
    return Book_service.get_book(db)

@app.post("/books", response_model=BookResponse)
def post_book(input_book: BookCreate,db:Session = Depends(get_db)):
    return Book_service.post_book(db, input_book)