from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Optional
from enum import Enum
import re

app = FastAPI(title="IT Asset Management API")

# --- 1. ENUMS & MODELS (Định nghĩa Dữ liệu & Ràng buộc) ---


class AssetStatus(str, Enum):
    READY = "READY"
    ALLOCATED = "ALLOCATED"
    REPAIRING = "REPAIRING"
    SCRAPPED = "SCRAPPED"


class Asset(BaseModel):
    id: int
    serial_number: str = Field(..., min_length=1)
    model: str = Field(..., min_length=2, max_length=255)
    stock_available: int = Field(..., ge=0)
    status: AssetStatus


class AssetUpdate(BaseModel):
    serial_number: Optional[str] = Field(None, min_length=1)
    model: Optional[str] = Field(None, min_length=2, max_length=255)
    stock_available: Optional[int] = Field(None, ge=0)
    status: Optional[AssetStatus] = None


class AllocationCreate(BaseModel):
    asset_id: int
    employee_email: str
    allocated_quantity: int = Field(..., gt=0)
    start_date: str  # Định dạng YYYY-MM-DD
    duration_months: int = Field(..., ge=1, le=12)

    # Validate Email bằng Regex chuẩn theo yêu cầu đề bài
    @field_validator("employee_email")
    @classmethod
    def validate_email_regex(cls, v: str) -> str:
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, v):
            raise ValueError("Định dạng email của nhân sự không hợp lệ.")
        return v


class Allocation(BaseModel):
    id: int
    asset_id: int
    employee_email: str
    allocated_quantity: int
    start_date: str
    duration_months: int


# --- 2. IN-MEMORY DATABASE (Dữ liệu mẫu) ---

assets_db = [
    {
        "id": 1,
        "serial_number": "SN-MAC-01",
        "model": "MacBook Pro M3",
        "stock_available": 5,
        "status": AssetStatus.READY,
    },
    {
        "id": 2,
        "serial_number": "SN-DELL-02",
        "model": "Dell UltraSharp 27",
        "stock_available": 10,
        "status": AssetStatus.READY,
    },
    {
        "id": 3,
        "serial_number": "SN-THINK-03",
        "model": "ThinkPad X1 Carbon",
        "stock_available": 0,
        "status": AssetStatus.REPAIRING,
    },
]

allocations_db = [
    {
        "id": 1,
        "asset_id": 1,
        "employee_email": "dev.nguyen@company.com",
        "allocated_quantity": 1,
        "start_date": "2026-07-01",
        "duration_months": 12,
    }
]

# --- 3. ASSETS ENDPOINTS (CRUD & Advanced Search) ---


@app.post("/assets", response_model=Asset, status_code=status.HTTP_201_CREATED)
def create_asset(asset: Asset):
    # Kiểm tra trùng lặp serial_number
    if any(a["serial_number"] == asset.serial_number for a in assets_db):
        raise HTTPException(
            status_code=400,
            detail="Mã thiết bị (serial_number) đã tồn tại trên hệ thống.",
        )

    # Kiểm tra trùng lặp ID
    if any(a["id"] == asset.id for a in assets_db):
        raise HTTPException(status_code=400, detail="ID tài sản đã tồn tại.")

    new_asset = asset.dict()
    assets_db.append(new_asset)
    return new_asset


@app.get("/assets", response_model=List[Asset])
def get_assets(
    keyword: Optional[str] = Query(
        None, description="Tìm kiếm theo serial_number hoặc model (Regex)"
    ),
    status: Optional[AssetStatus] = Query(None, description="Lọc theo trạng thái"),
    min_stock: Optional[int] = Query(
        None, ge=0, description="Số lượng tồn kho tối thiểu"
    ),
):
    filtered_assets = assets_db

    # Tìm kiếm nâng cao bằng Regex (không phân biệt chữ hoa chữ thường)
    if keyword:
        try:
            pattern = re.compile(keyword, re.IGNORECASE)
            filtered_assets = [
                a
                for a in filtered_assets
                if pattern.search(a["serial_number"]) or pattern.search(a["model"])
            ]
        except re.error:
            raise HTTPException(
                status_code=400, detail="Biểu thức chính quy (Regex) không hợp lệ."
            )

    # Lọc theo status
    if status:
        filtered_assets = [a for a in filtered_assets if a["status"] == status]

    # Lọc theo min_stock
    if min_stock is not None:
        filtered_assets = [
            a for a in filtered_assets if a["stock_available"] >= min_stock
        ]

    return filtered_assets


@app.get("/assets/{asset_id}", response_model=Asset)
def get_asset_by_id(asset_id: int):
    for asset in assets_db:
        if asset["id"] == asset_id:
            return asset
    raise HTTPException(status_code=404, detail="Asset not found")


@app.put("/assets/{asset_id}", response_model=Asset)
def update_asset(asset_id: int, updated_fields: AssetUpdate):
    for asset in assets_db:
        if asset["id"] == asset_id:
            # Kiểm tra duy nhất serial_number nếu có cập nhật trường này
            if updated_fields.serial_number:
                if any(
                    a["serial_number"] == updated_fields.serial_number
                    and a["id"] != asset_id
                    for a in assets_db
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="Mã thiết bị (serial_number) đã tồn tại.",
                    )

            # Cập nhật các trường được gửi lên
            update_data = updated_fields.dict(exclude_unset=True)
            for key, value in update_data.items():
                asset[key] = value
            return asset

    raise HTTPException(status_code=404, detail="Asset not found")


@app.delete("/assets/{asset_id}", status_code=status.HTTP_200_OK)
def delete_asset(asset_id: int):
    for index, asset in enumerate(assets_db):
        if asset["id"] == asset_id:
            assets_db.pop(index)
            return {"detail": f"Xóa thành công tài sản ID {asset_id}"}
    raise HTTPException(status_code=404, detail="Asset not found")


# --- 4. ALLOCATIONS ENDPOINTS (Nghiệp vụ Cấp phát) ---


@app.post(
    "/allocations", response_model=Allocation, status_code=status.HTTP_201_CREATED
)
def create_allocation(allocation: AllocationCreate):
    # Quy tắc 1: asset_id cấp phát bắt buộc phải tồn tại
    target_asset = None
    for asset in assets_db:
        if asset["id"] == allocation.asset_id:
            target_asset = asset
            break

    if not target_asset:
        raise HTTPException(
            status_code=400,
            detail="Thiết bị (asset_id) không tồn tại trong danh mục công ty.",
        )

    # Quy tắc 2: Thiết bị bàn giao phải có trạng thái kho là "READY"
    if target_asset["status"] != AssetStatus.READY:
        raise HTTPException(
            status_code=400,
            detail=f"Không thể cấp phát. Thiết bị hiện đang ở trạng thái: {target_asset['status']}.",
        )

    # Quy tắc 4: Số lượng yêu cầu không vượt quá tồn kho khả dụng thực tế
    if allocation.allocated_quantity > target_asset["stock_available"]:
        raise HTTPException(
            status_code=400,
            detail=f"Số lượng yêu cầu ({allocation.allocated_quantity}) vượt quá tồn kho khả dụng ({target_asset['stock_available']}).",
        )

    # --- XỬ LÝ CẬP NHẬT TRẠNG THÁI & KHO ---
    target_asset["stock_available"] -= allocation.allocated_quantity
    if target_asset["stock_available"] == 0:
        target_asset["status"] = AssetStatus.ALLOCATED

    # Tạo bản ghi cấp phát mới
    new_id = max([a["id"] for a in allocations_db]) + 1 if allocations_db else 1
    new_allocation = {
        "id": new_id,
        "asset_id": allocation.asset_id,
        "employee_email": allocation.employee_email,
        "allocated_quantity": allocation.allocated_quantity,
        "start_date": allocation.start_date,
        "duration_months": allocation.duration_months,
    }
    allocations_db.append(new_allocation)

    return new_allocation


@app.get("/allocations", response_model=List[Allocation])
def get_allocations():
    return allocations_db