from sqlalchemy.orm import Session
from schemas import BookCreate
from models import BookModel

def Post_book(input_book: BookCreate,db:Session):
    new_book = BookModel(
        title = input_book.title,
        author = input_book.author,
        category = input_book.category,
        price = input_book.price,
        borrow_count = input_book.borrow_count,
        available_quantity = input_book.available_quantity
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

def Get_books(db:Session):
    books = db.query(BookModel).all()
    return books

def Borrow_warning(threshold: int, db: Session):

    books = db.query(BookModel).filter(
        BookModel.available_quantity <= threshold
    ).all()

    return books

def get_search_book(query:str, db:Session):
    find_name = db.query(BookModel).filter(
        BookModel.title.ilike(f"%{query}%") |
        BookModel.author.ilike(f"%{query}%") |
        BookModel.category.ilike(f"%{query}%")
        ).all()
    return find_name

def Top_borrowed(limit: int, db: Session):

    books = db.query(BookModel).order_by(
        BookModel.borrow_count.desc()
    ).limit(limit).all()

    return books

def Get_book_id(id:int,db:Session):
    find_id = db.query(BookModel).filter(BookModel.id == id).first()
    return find_id

def Put_book(id:int,input_book: BookCreate,db:Session):
    find_id = db.query(BookModel).filter(BookModel.id == id).first()
    if not find_id:
        return None
    data = input_book.model_dump()

    for key, value in data.items():
        setattr(find_id, key, value)

    db.commit()
    db.refresh(find_id)

    return find_id

def Delete_book(id:int,db:Session):
    find_id = db.query(BookModel).filter(BookModel.id == id).first()
    if not find_id:
        return None
    db.delete(find_id)
    db.commit()
    return{
        "message": "đã xóa thành công!"
    }


