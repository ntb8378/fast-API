# | STT | Dữ liệu gửi lên                       | Kết quả hiện tại           | Kết quả đúng mong muốn                            | Lỗi phát hiện                |
# | --- | ------------------------------------- | -------------------------- | ------------------------------------------------- | ---------------------------- |
# | 1   | `student_id = "SV001", course_id = 1` | API vẫn đăng ký thành công | API phải báo lỗi học viên đã đăng ký khóa học này | Không kiểm tra đăng ký trùng |
# | 2   | `student_id = "SV002", course_id = 1` | API vẫn đăng ký thành công | API phải báo lỗi học viên đã đăng ký khóa học này | Không kiểm tra đăng ký trùng |


# phần 2:
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

enrollments = [
    {
        "id": 1,
        "student_id": "SV001",
        "course_id": 1
    },
    {
        "id": 2,
        "student_id": "SV002",
        "course_id": 1
    }
]

class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: int

# Sửa: thêm status_code=201 để trả về HTTP 201 Created
@app.post("/enrollments", status_code=status.HTTP_201_CREATED)
def create_enrollment(enrollment: EnrollmentCreate):

    # Sửa: kiểm tra học viên đã đăng ký khóa học này chưa
    for e in enrollments:
        if e["student_id"] == enrollment.student_id and e["course_id"] == enrollment.course_id:
            # Sửa: nếu đã đăng ký thì trả về lỗi
            raise HTTPException(
                status_code=400,
                detail="Student has already enrolled in this course"
            )

    new_enrollment = {
        "id": len(enrollments) + 1,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id
    }

    enrollments.append(new_enrollment)

    return {
        "message": "Enroll successfully",
        "data": new_enrollment
    }