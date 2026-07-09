from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from datetime import datetime

# --- BASE SCHEMA ---
class BoardingSlotBase(BaseModel):
    slot_number: str = Field(..., max_length=50, description="Mã số khoang chuồng")
    room_size: str = Field(..., description="Kích thước phòng: SMALL, MEDIUM, LARGE")
    price_per_day: float = Field(..., gt=0.0, description="Giá thuê mỗi ngày phải lớn hơn 0")
    status: str = Field(default="VACANT", description="Trạng thái: VACANT hoặc OCCUPIED")

    @field_validator('room_size')
    @classmethod
    def validate_room_size(cls, v: str) -> str:
        valid_sizes = {"SMALL", "MEDIUM", "LARGE"}
        if v not in valid_sizes:
            raise ValueError("room_size chỉ được nhận các giá trị: SMALL, MEDIUM, LARGE")
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        valid_statuses = {"VACANT", "OCCUPIED"}
        if v not in valid_statuses:
            raise ValueError("status chỉ được nhận các giá trị: VACANT, OCCUPIED")
        return v

# --- REQUEST SCHEMAS ---
class BoardingSlotCreate(BoardingSlotBase):
    pass

class BoardingSlotUpdate(BoardingSlotBase):
    pass

# --- RESPONSE DATA SCHEMA ---
class BoardingSlotResponseData(BoardingSlotBase):
    id: int

    class Config:
        from_attributes = True

# --- UNIFIED RESPONSE SCHEMA (6 TRƯỜNG BẮT BUỘC) ---
class UnifiedResponse(BaseModel):
    statusCode: int
    message: str
    error: Optional[str] = None
    data: Optional[Any] = None
    path: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))