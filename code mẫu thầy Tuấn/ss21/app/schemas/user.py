from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    # Dữ liệu đầu vào khi đăng ký cần có mật khẩu thô
    password: str

class UserLogin(UserBase):
    # Dữ liệu đầu vào khi đăng nhập
    password: str

class UserResponse(UserBase):
    # Dữ liệu trả về cho client, TUYỆT ĐỐI KHÔNG trả về mật khẩu
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        # Pydantic V2 cấu hình từ form_attributes (ở V1 là orm_mode = True)
        # Giúp Pydantic có thể đọc dữ liệu trực tiếp từ SQLAlchemy Model object
        from_attributes = True
