from pydantic import Field, BaseModel, ConfigDict
from typing import Optional

class WarehouseCreate(BaseModel):
    warehouse_name : str = Field( ... ,min_length=5)
    location : str = Field( ... ,min_length=5)

class PackageResponse(BaseModel):
    id: int
    package_code : str
    weight: float

class WarehouseDetailResponse(BaseModel):
    warehouse_name : str
    location : str
    packages : list[PackageResponse]
    model_config = ConfigDict(from_attributes=True)

class PackageUpdate(BaseModel):
    package_code : Optional[str] = Field(None)
    weight : Optional[int] = Field(None)

class WaybillResponse(BaseModel):
    tracking_number: str
    shipping_status : str
    model_config = ConfigDict(from_attributes=True)