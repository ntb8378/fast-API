from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import schemas
import crud

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Classroom Student Management API")

@app.post("/classrooms", status_code=status.HTTP_201_CREATED)
def create_classroom(data: schemas.ClassroomCreate, db: Session = Depends(get_db)):
    return crud.create_classroom(db=db, data=data)

@app.post("/students", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(data: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db=db, data=data)

@app.get("/classrooms/{classroom_id}", response_model=schemas.ClassroomDetailResponse)
def get_classroom_detail(classroom_id: int, db: Session = Depends(get_db)):
    return crud.get_classroom_detail(db=db, classroom_id=classroom_id)

@app.put("/students/{student_id}/transfer", response_model=schemas.StudentResponse)
def transfer_student(student_id: int, data: schemas.TransferClassRequest, db: Session = Depends(get_db)):
    return crud.transfer_student(db=db, student_id=student_id, data=data)