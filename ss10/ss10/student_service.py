from sqlalchemy.orm import Session
from model import *

def create_students(db: Session, student: StudentRequetsDTO):
    try:
        new_student = StudentModel(
            id = student.id,
            full_name = student.full_name,
            email = student.email
        )
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

        return {
            "status_code": 201,
            "message": "Tao sinh vien thanh cong"
        }
    except Exception as e:
        db.rollback()
        raise ValueError(f"Loi khi tao sinh vien: {str(e)}")