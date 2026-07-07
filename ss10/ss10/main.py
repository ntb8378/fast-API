from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from sqlalchemy import text
from model import *
from student_service import create_students

app = FastAPI()

Base.metadata.create_all(bind = engine)

@app.get("/test_conections")
def test_connection(db: Session = Depends(get_db)):
    try:
        db.execute(text('SELECT 1'))

        return {
            "status_code": 200,
            "message": "Lay du lieu thanh cong"
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Loi khoong ket noi duoc")

@app.post("/students")
def add_students(student: StudentRequetsDTO, db: Session = Depends(get_db)):
    result = create_students(db=db, student=student)

    return result
