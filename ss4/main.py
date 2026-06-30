from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI(
title = "Manager Student",
description = "Đây là API cung cấp để quản lý sinh viên cá biệt",
version = "1.0.0"
)

# Ví dụ danh sách sv này được lấy từ database về
student_dtb = [
{"id": "sv001", "username": "vietthanh", "password": "123"},
{"id": "sv002", "username": "giahung", "password": "456"}
]
#Tạo API để lấy danh sách sinh viên
@app.get("/students", tags=["Students"], summary="Lấy ds sinh viên")
def get_all_students():
    return {
    "status_code": 200,
    "message": "Lay danh sach sinh vien thanh công",
    "data": student_dtb
    }

# Định hình dữ liệu người dùng nhập vào
class StudentSchema (BaseModel) :
    id: int
    username: str
    pafsword: str
