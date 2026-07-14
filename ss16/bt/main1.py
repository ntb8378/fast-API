from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class StudentCreate(BaseModel):
    student_code: str
    full_name: str
    class_id: int

classrooms = [
    {
        "id": 1,
        "name": "FastAPI Basic",
        "max_students": 2,
        "status": "OPEN"
    },
    {
        "id": 2,
        "name": "Python Foundation",
        "max_students": 3,
        "status": "CLOSED"
    }
]

students = [
    {
        "id": 1,
        "student_code": "SV001",
        "full_name": "Nguyễn Văn An",
        "class_id": 1
    },
    {
        "id": 2,
        "student_code": "SV002",
        "full_name": "Trần Minh Bình",
        "class_id": 1
    }
]

@app.get("/classrooms")
def get_classrooms():
    return classrooms

@app.get("/students")
def get_students():
    return students

@app.post(
    "/students",
    status_code=status.HTTP_201_CREATED
)
def create_student(student_data: StudentCreate):
    # 1. Kiểm tra lớp học tồn tại hay không
    classroom = next(
        (
            classroom
            for classroom in classrooms
            if classroom["id"] == student_data.class_id
        ),
        None
    )

    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lớp học không tồn tại"
        )

    # 2. Kiểm tra trạng thái lớp học (Chỉ chấp nhận OPEN)
    if classroom["status"] != "OPEN":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lớp học không ở trạng thái mở (OPEN)"
        )

    # 3. Kiểm tra số lượng sinh viên tối đa (Sử dụng dấu >= thay vì >)
    current_students = [
        student
        for student in students
        if student["class_id"] == student_data.class_id
    ]

    if len(current_students) >= classroom["max_students"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lớp học đã đủ số lượng sinh viên"
        )

    # 4. Kiểm tra trùng mã sinh viên trên toàn hệ thống (Bỏ điều kiện trùng class_id)
    duplicated_student = next(
        (
            student
            for student in students
            if student["student_code"] == student_data.student_code
        ),
        None
    )

    if duplicated_student:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Mã sinh viên đã tồn tại trên hệ thống"
        )

    # 5. Tạo mới sinh viên thành công
    new_student = {
        "id": len(students) + 1,
        "student_code": student_data.student_code,
        "full_name": student_data.full_name,
        "class_id": student_data.class_id
    }

    students.append(new_student)
    return new_student