from sqlalchemy.orm import Session
from schemas import BookCreate
from models import Book

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
    return db.query(Book).filter(Book.id == id).first()

def put_book_id(db: Session , id : int, book: BookCreate):
    return db.query(Book).filter(Book.id == id).first()
