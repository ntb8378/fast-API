from sqlalchemy.orm import Session
from models import BookModel
from schemas import BookCreate

def get_book(db:Session):
    return db.query(BookModel).all()

def post_book(db:Session, input_book:BookCreate):
    new_book = BookModel(
        code  =input_book.code,
        title = input_book.title,
        price = input_book.price,
        pages =input_book.pages
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book