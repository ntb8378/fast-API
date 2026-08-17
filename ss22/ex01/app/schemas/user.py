from pydantic import BaseModel
from pydantic import ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password : str

class UserResponse(BaseModel):
    """Lớp trả về"""

    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)