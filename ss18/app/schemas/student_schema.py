# pyrefly: ignore [missing-import]
from pydantic import BaseModel

# Model base dùng chung, muốn dùng cho nhưng tính năng khác thì phải kế thừa rồi viết lại
class StudentBase(BaseModel):
    name: str
    age: int

class StudentCreateDTO(StudentBase):
    pass

class StudentputDTO(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True
        