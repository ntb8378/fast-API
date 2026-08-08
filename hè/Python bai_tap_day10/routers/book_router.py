from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.schemas import BookUpdate
import service.book_service as book_service

router = APIRouter(
    prefix="/api/v1/books",
    tags=["Book Controller"]
)


@router.put("/{id}")
def update_book(id:int,book_in: BookUpdate,db: Session = Depends(get_db)):
    update_book= book_service.update_book(db, id,book_in)
    if update_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sách không tồn tại trong hệ thống")
    return update_book 

@router.delete("/{id}")
def api_delete_book(id: int, db: Session = Depends(get_db)):
    success = book_service.delete_book(db,id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sách không tồn tại trong hệ thống")
    return {
        "message": f"Đã xóa thành công sách ID {id}"
    }