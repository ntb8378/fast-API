from sqlalchemy.orm import Session
from app.models.student_model import StudentModel

def get_all_student(db: Session):
    return db.query(StudentModel).all()