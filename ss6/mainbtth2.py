from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]


class CreateStudent(BaseModel):
    code: str
    name: str
    email: str
    age: int = Field(..., gt=0)


class UpdateStudent(BaseModel):
    code: str
    name: str
    email: str
    age: int = Field(..., gt=0)


@app.get("/")
def root():
    return {"message": "Hello"}


# Lấy danh sách + tìm kiếm + lọc
@app.get("/students")
def get_students(keyword: str = None, min_age: int = None, max_age: int = None):

    result = students

    if keyword:
        result = [
            student for student in result
            if keyword.lower() in student["name"].lower()
            or keyword.lower() in student["code"].lower()
            or keyword.lower() in student["email"].lower()
        ]

    if min_age is not None:
        result = [
            student for student in result
            if student["age"] >= min_age
        ]

    if max_age is not None:
        result = [
            student for student in result
            if student["age"] <= max_age
        ]

    return result


# Lấy chi tiết học viên
@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(status_code=404, detail="Không tìm thấy học viên")


# Thêm học viên
@app.post("/students")
def create_student(student: CreateStudent):

    new_id = max((s["id"] for s in students), default=0) + 1

    new_student = {
        "id": new_id,
        "code": student.code,
        "name": student.name,
        "email": student.email,
        "age": student.age
    }

    students.append(new_student)

    return new_student


# Cập nhật học viên
@app.put("/students/{student_id}")
def update_student(student_id: int, update_student: UpdateStudent):

    for student in students:
        if student["id"] == student_id:

            student["code"] = update_student.code
            student["name"] = update_student.name
            student["email"] = update_student.email
            student["age"] = update_student.age

            return student

    raise HTTPException(status_code=404, detail="Không tìm thấy học viên")


# Xóa học viên
@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return {"message": "Xóa học viên thành công"}

    raise HTTPException(status_code=404, detail="Không tìm thấy học viên")