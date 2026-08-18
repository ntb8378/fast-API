from fastapi import FastAPI
from app.db.database import engine, Base
from app.routers import auth

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Demo Authentication FastAPI",
    description="Ứng dụng mẫu Đăng ký và Đăng nhập với FastAPI và MySQL dành cho sinh viên.",
    version="1.0.0"
)

# Tạo tất cả các bảng trong Database (nếu chưa có)
# Lưu ý: Trong thực tế dự án lớn thường dùng thư viện Alembic để quản lý database migration thay vì tạo trực tiếp.
Base.metadata.create_all(bind=engine)

# Nhúng router xử lý auth vào ứng dụng chính
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Chào mừng đến với API Authentication Demo. Hãy truy cập /docs để test."}

# --- HƯỚNG DẪN DÀNH CHO SINH VIÊN ---
# 1. Tạo và kích hoạt môi trường ảo (Virtual Environment):
#    - macOS/Linux: python3 -m venv venv && source venv/bin/activate
#    - Windows: python -m venv venv && venv\Scripts\activate
# 2. Cài đặt thư viện: 
#    pip install -r requirements.txt
# 3. Mở MySQL, tạo Database: 
#    CREATE DATABASE student_db;
# 4. Mở file app/db/database.py cập nhật thông tin DATABASE_URL cho khớp với MySQL của máy mình.
# 5. Chạy server bằng Uvicorn: 
#    uvicorn app.main:app --reload
# 6. Truy cập Swagger UI để test API: 
#    http://127.0.0.1:8000/docs
