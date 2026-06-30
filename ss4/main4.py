"""
Phần 1: Phân tích & Đề xuất đa giải pháp
Input:

Request body JSON chứa thông tin học viên: full_name, email, age, course, phone.

Output:

Thành công: Trả về thông tin học viên vừa đăng ký.

Thất bại: Trả về lỗi rõ ràng (thiếu trường, sai định dạng email, email trùng).

Giải pháp 1: Dùng Pydantic BaseModel + Field

Khai báo model với các ràng buộc (min_length, EmailStr).

FastAPI tự động validate và trả lỗi 422 nếu dữ liệu không hợp lệ.

Kiểm tra email trùng bằng logic trong hàm.

Giải pháp 2: Dùng dict tự do + kiểm tra thủ công

Nhận dữ liệu dạng dict.

Tự viết code kiểm tra từng trường (rỗng, độ dài, regex email, trùng email).

Chủ động kiểm soát lỗi nhưng nhiều code hơn.

Phần 2: So sánh & Lựa chọn
Tiêu chí	            |Giải pháp 1: Pydantic	            |Giải pháp 2: dict thủ công
Độ dễ hiểu	            |Rõ ràng, ngắn gọn	                |Phức tạp hơn
Số lượng code	        |Ít, tận dụng validation tự động	|Nhiều, phải viết tay
Khả năng kiểm soát lỗi	|Tốt, chuẩn REST (422)	            |Linh hoạt nhưng dễ sai sót
Độ rõ ràng dữ liệu	    |Có schema rõ ràng	                |Không có schema
"""
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

# Danh sách email đã tồn tại
existing_emails = {"existing@gmail.com"}

class Student(BaseModel):
    full_name: str = Field(..., min_length=3)
    email: EmailStr
    age: int
    course: str
    phone: str

@app.post("/students")
def create_student(student: Student):
    # Kiểm tra email trùng
    if student.email in existing_emails:
        return {"detail": "Email đã tồn tại trong hệ thống"}
    
    # Thêm email vào danh sách giả lập
    existing_emails.add(student.email)
    return student
