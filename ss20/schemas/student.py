from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from schemas.classroom import ClassroomResponse


class StudentBase(BaseModel):
    student_code: str = Field(..., min_length=3, max_length=20)
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=16, le=60)
    gender: Literal["male", "female", "other"]
    class_id: int = Field(..., ge=1)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class StudentResponse(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    classroom: Optional[ClassroomResponse] = None
