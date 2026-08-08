from fastapi import FastAPI, Depends, HTTPException, status
from database import Base, engine, get_db
from models import BookModel
from sqlalchemy.orm import Session
import book_service
from schemas import BookUpdate

app = FastAPI()

Base.metadata.create_all(bind= engine)


@app.get("/")
def test():
    return {
        "message": "kết nối thành công!"
    }

@app.put("/books/{id}")
def update_book(id:int,book_in: BookUpdate,db: Session = Depends(get_db)):
    update_book= book_service.update_book(db, id,book_in)
    if update_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sách không tồn tại trong hệ thống")
    return update_book 

@app.delete("/books/{id}")
def api_delete_book(id: int, db: Session = Depends(get_db)):
    success = book_service.delete_book(db,id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sách không tồn tại trong hệ thống")
    return {
        "message": f"Đã xóa thành công sách ID {id}"
    }