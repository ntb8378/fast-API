from fastapi import FastAPI, Depends, HTTPException
from database import get_db, engine, base
from sqlalchemy import text
from sqlalchemy.orm import Session
import models
from schemas import BookCreate
import crud

app = FastAPI(
    title="LIBRARY MANAGEMENT"
)

base.metadata.create_all(engine)

@app.get("/test")
def test(db: Session = Depends(get_db)):
    try:
        db.execute(text("Select 1"))

        return {
            "message": "kết nối thành công!"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="kết nối thất bại")
    
@app.post("/books")
def post_books(
    book: BookCreate,
    db: Session = Depends(get_db)
):
    return crud.create_book(db , book)


@app.get("/books")
def get_books(
    db: Session = Depends(get_db)
):
    return crud.get_book(db)

@app.get("/books/{id}")
def get_book_id(
    id: int,
    db:Session = Depends(get_db)
):
    return crud.get_book_id(db, id)