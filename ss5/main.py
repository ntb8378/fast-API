from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="Manager Student",
    description="Đây là API cung cấp để quản lý sinh viên cá biệt",
    version="1.0.0"
)

# Ví dụ danh sách sinh viên lấy từ database
student_dtb = [
    {"id": 1, "username": "vietthanh", "password": "123"},
    {"id": 2, "username": "giahung", "password": "456"},
    {"id": 3, "username": "giabao", "password": "765"},
    {"id": 4, "username": "giaanh", "password": "899"}
]

# Định nghĩa dữ liệu người dùng nhập vào
class StudentSchema(BaseModel):
    username: str = Field(..., min_length=4, max_length=20)
    password: str


# API tạo sinh viên
@app.post("/students", tags=["Students"], status_code=status.HTTP_201_CREATED)
def create_students(student: StudentSchema):

    new_student = {
        "id": len(student_dtb) + 1,
        "username": student.username,
        "password": student.password
    }

    student_dtb.append(new_student)

    return {
        "status_code": 201,
        "message": "Them thanh cong",
        "data": new_student
    }


# API lấy 1 sinh viên
@app.get("/students/{student_id}", tags=["Students"])
def get_student_by_id(student_id: int):

    for student in student_dtb:
        if student.get("id") == student_id:
            return {
                "message": "Lay thanh cong",
                "data": student
            }

    return {
        "message": "Khong tim thay"
    }


# Lấy nhiều sinh viên kèm điều kiện (Query Parameter)
@app.get("/students", tags=["Students"], summary="Lấy ds theo điều kiện")
def get_students(
    keyword: Optional[str] = "",
    limit: int = 10
):

    list_student = []

    for student in student_dtb:
        if keyword.lower() in student.get("username").lower():
            list_student.append(student)

    result = list_student[:limit]

    return {
        "status_code": 200,
        "message": "Lay du lieu thanh cong",
        "data": result
    }

# Câu 1: API xóa sinh viên theo id
@app.delete("/students/{student_id}", tags=["Students"])
def delete_student(student_id: int):

    for student in student_dtb:
        if student.get("id") == student_id:
            student_dtb.remove(student)

            return {
                "status_code": 200,
                "message": "Xoa thanh cong",
                "data": student
            }

    raise HTTPException(
        status_code = 404,
        detail = "không tìm thấy"
    )


# Câu 2: API cập nhật thông tin sinh viên theo id
@app.put("/students/{student_id}", tags=["Students"])
def update_student(student_id: int, student: StudentSchema):

    for old_student in student_dtb:
        if old_student.get("id") == student_id:

            old_student.update({
                "username": student.username,
                "password": student.password
            })

            return {
                "status_code": 200,
                "message": "Cap nhat thanh cong",
                "data": old_student
            }

    return {
        "status_code": 404,
        "message": "Khong tim thay sinh vien"
    }