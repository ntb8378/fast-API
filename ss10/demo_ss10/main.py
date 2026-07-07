from fastapi import FastAPI,Depends,HTTPException,status
from sqlalchemy.orm import Session
from database import get_db,Base,engine
from sqlalchemy import text
import model
from pydantic import BaseModel
from  student_service import create_student,get_student,get_all


#Lệnh yêu cầu sqlalchemy nó quét tất cả các model đã import và tạo bảng tương ứng nếu ch tồn tại
Base.metadata.create_all(bind = engine)

app = FastAPI()

class StudentCreate(BaseModel):
    id: int
    full_name: str
    email: str


def root():
    return {"message": "Xin chao Viet thanh"}

@app.get("/testconection")
def test_connection(db: Session = Depends(get_db)):
    try:
        # Thuc hien cau lenh truy van don gian
        db.execute(text("SELECT 1"))

        return {
            "status": "success",
            "message": "Ket noi thanh cong"
        }
    except Exception as e:
        raise HTTPException (
            status_code=500,
            detail=f"KET NOI THAT BAI. LOI: {str(e)}"
        )


@app.post("/student",status_code=status.HTTP_201_CREATED)
def create_student_function(student: StudentCreate, db: Session = Depends(get_db)):
    result = create_student(
        db=db,
        id= student.id,
        fullname=student.full_name,
        email=student.email,
    )

    return {
        "message": "Them sinh vien thanh cong",
        "data": result
    }


@app.get("/student/{student_id}",status_code=status.HTTP_200_OK)
def get_student_detail(student_id: int, db:Session = Depends(get_db)):
    result = get_student(db,student_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not FOUNDS"
        )

    return {
        "message": 'Lay thong tin thanh cong',
        "data": result
    }

@app.get("/student",status_code=status.HTTP_200_OK)
def get_all_stu(db: Session = Depends(get_db)):
    result =  get_all(db)

    return {
        "message": "LAY THANH CONG TAT CA THONG TIN SINH VIEN",
        "DATA": result
    }

