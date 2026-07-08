# file này dùng để cấu hình DTO - những khuôn dữ liệu ngươi dùng
from pydantic import BaseModel

class UsersRequestDTO(BaseModel):
    name: str
    email: str
    