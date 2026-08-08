from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import BookCreate
import book_service

router = APIRouter(
    prefix= "/api/v1/books",
    tags=["Books"]
)

@router.post("/", status_code=201)
def Post_book(input_book:BookCreate,db:Session = Depends(get_db)):
    return book_service.Post_book(input_book, db)

@router.get("/",status_code= 200)
def Get_books(db:Session = Depends(get_db)):
    return book_service.Get_books(db)

@router.get("/borrow-warning")
def Borrow_warning(threshold: int = 5,db: Session = Depends(get_db)):
    return book_service.Borrow_warning(threshold, db)


@router.get("/search")
def get_search_book(query:str, db:Session = Depends(get_db)):
    find_name= book_service.get_search_book(query, db)
    if not find_name:
            raise HTTPException(
                status_code=404,
                detail="Không tìm thấy sách"
            )
    return find_name

@router.get("/top-borrowed")
def Top_borrowed(
    limit: int = 5,
    db: Session = Depends(get_db)
):
    return book_service.Top_borrowed(limit, db)

@router.get("/{id}")
def Get_book_id(id:int,db:Session = Depends(get_db)):
    find_id= book_service.Get_book_id(id, db)
    if not find_id:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sách"
        )
    return find_id

@router.put("/{id}")
def Put_book(id:int ,input_book:BookCreate,db:Session = Depends(get_db)):
    find_id = book_service.Put_book(id, input_book, db)
    if not find_id:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sách"
        )
    return find_id

@router.delete("/{id}")
def Delete_book(id:int,db: Session = Depends(get_db)):
    find_id= book_service.Delete_book(id, db)
    if not find_id:
            raise HTTPException(
                status_code=404,
                detail="Không tìm thấy sách"
            )
    return {
         "message": f"đã xóa id{find_id}"
    }

