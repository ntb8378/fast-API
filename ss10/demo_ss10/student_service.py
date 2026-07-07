from sqlalchemy.orm import Session
from model import StudentModel

def create_student(db: Session, id: int, fullname: str, email: str):
    new_student = StudentModel(
        id= id,
        fullname= fullname,
        email= email
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

def get_student(db: Session,id:int):
# Lay thong tin chi tiet database

    return(
        db.query(StudentModel)
        .filter(StudentModel.id == id)
        .first()
    )

def get_all(db: Session):
    #LAY TAT CA THONG TIN SINH VIEN DATABASE
    return db.query(StudentModel).all()
