from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="API quản lý sinh viên",
    description="đây là api để cung cấp client cho việc quản lý sinh viên",
    version="1.0.0",
)
# tạo ra khung sườn thuộc tính của dự án để pydantic swagger tự động kiểm tra trước khi gửi đi dữ liệu
class StudentChema(BaseModel):
    username : str
    password : str
    phone : str

student_database = {
    1:{"username": "Huy", "password": "123", "phone": "0987"},
    2:{"username": "Tân", "password": "456", "phone": "0978"}
}
@app.get("/students")
def get_all_student():
    return student_database.values()

@app.post("/students", tags=["Student"], summary="Thêm sinh viên")
def create_student(student: StudentChema):
    student_id = len(student_database) + 1
    new_student = {
        "username": student.username,
        "password": student.password,
        "phone": student.phone
    }

    student_database[student_id] = new_student
    return {
        "status_code": 201,
        "message": "thêm sinh viên thành công!",
        "data": new_student
    }

@app.get("/")
def get_root():
    return student_database