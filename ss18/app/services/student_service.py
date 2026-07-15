from sqlalchemy.orm import Session, joinedload
from app.models.student_model import StudentModel

def get_all_student(db: Session, offset:int , limit : int):
    # return db.query(StudentModel).all()

    return db.query(StudentModel).options(joinedload(StudentModel.department)).offset(offset).limit(limit).all()