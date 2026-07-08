from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime, timezone


class ParkingSlotBase(BaseModel):
    """Định dạng dữ liệu"""

    slot_code: str = Field(..., description="Mã vị trí đõ(Duy nhất)")
    zone_name: str = Field(..., min_length=3, description="Tên khu vục(Tối thiểu là 3)")
    max_weight: int = Field(..., gt=0, description="Tải trọng tối da phải lớn hơn 0")
    is_available: bool = Field(default=True)


class ParkingSlotCreate(ParkingSlotBase):
    """Tạo"""


class ParkingSlotResponseData(ParkingSlotBase):
    id: int

    model_config = {"from_attributes": True}


class StandarResponse(BaseModel):
    statusCode: int
    message: str
    error: Optional[str] = None
    data: Any
    path: str
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
