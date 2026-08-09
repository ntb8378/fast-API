from sqlalchemy.orm import Session
from schemas import BookCreate
from models import BookModel
from models import AuthorModel
from fastapi import HTTPException

def create_book(db: Session, book_in: BookCreate):

    # 1. Kiểm tra author_id có tồn tại không
    author = db.query(AuthorModel).filter(
        AuthorModel.id == book_in.author_id
    ).first()

    # 2. Nếu không tồn tại -> báo lỗi 400
    if not author:
        raise HTTPException(
            status_code=400,
            detail=f"Mã tác giả author_id = {book_in.author_id} không tồn tại trong hệ thống CSDL!"
        )

    # 3. Tạo đối tượng BookModel
    db_book = BookModel(
        title=book_in.title,
        author_id=book_in.author_id,
        category=book_in.category,
        price=book_in.price,
        borrow_count=book_in.borrow_count,
        available_quantity=book_in.available_quantity
    )

    # 4. Thêm vào database
    db.add(db_book)

    # 5. Lưu database
    db.commit()

    # 6. Cập nhật lại object từ database
    db.refresh(db_book)

    # 7. Trả về sách vừa tạo
    return db_book

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


