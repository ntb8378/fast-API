# app/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional


# --- WAYBILL SCHEMAS ---
class WaybillBase(BaseModel):
    tracking_number: str
    shipping_status: str


class WaybillResponse(WaybillBase):
    id: int
    package_id: int

    class Config:
        from_attributes = True


# --- PACKAGE SCHEMAS ---
class PackageBase(BaseModel):
    package_code: str
    weight: float


class PackageCreate(PackageBase):
    warehouse_id: int


class PackageUpdate(BaseModel):
    package_code: Optional[str] = Field(None, min_length=1)
    weight: Optional[float] = Field(None, gt=0)
    warehouse_id: Optional[int] = None


class PackageResponse(PackageBase):
    id: int
    warehouse_id: int

    class Config:
        from_attributes = True


# --- WAREHOUSE SCHEMAS ---
class WarehouseCreate(BaseModel):
    warehouse_name: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)


class WarehouseDetailResponse(BaseModel):
    id: int
    warehouse_name: str
    location: str
    packages: List[PackageResponse] = []  # Lồng ghép danh sách các kiện hàng liên kết

    class Config:
        from_attributes = True
