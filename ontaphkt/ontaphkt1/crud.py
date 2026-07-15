from sqlalchemy.orm import Session
from schemas import BookCreate
from models import Book
from fastapi import HTTPException

def create_book(db: Session , book: BookCreate):
    db_book = Book(
        title = book.title,
        author = book.author,
        isbn = book.isbn,
        status = book.status
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book

def get_book(db: Session):  
    return db.query(Book).all()

def get_book_id(db: Session , id : int):
    db_book= db.query(Book).filter(Book.id == id).first()
    if not db_book:
        raise HTTPException(
    status_code=404,
    detail="Book not found"
)
    return db_book

def put_book_id(db: Session , id : int, book: BookCreate):
    db_book= db.query(Book).filter(Book.id == id).first()
    db_book.title = book.title
    db_book.author = book.author
    db_book.status = book.status

    db.commit()
    db.refresh(db_book)

    return db_book

def delete_books_id(db: Session , id:int):
    db_book = db.query(Book).filter(Book.id == id).first()
    db.delete(db_book)

    db.commit()

    return {"message": "Delete success"}