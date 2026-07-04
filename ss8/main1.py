from datetime import date
from enum import Enum
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(title="Logistics Management API")
class CarrierStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class ShiftEnum(str, Enum):
    MORNING = "MORNING"
    AFTERNOON = "AFTERNOON"
    NIGHT = "NIGHT"


class CarrierCreate(BaseModel):
    code: str = Field(..., description="Mã đối tác (Unique không rỗng)")
    name: str = Field(..., min_length=3, description="Tên đối tác tối thiểu 3 ký tự")
    max_weight_capacity: int = Field(
        ..., gt=0, description="Tải trọng tối đa phải lớn hơn 0"
    )
    status: CarrierStatus


class CarrierUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3)
    max_weight_capacity: Optional[int] = Field(None, gt=0)
    status: Optional[CarrierStatus] = None


class ShipmentCreate(BaseModel):
    carrier_id: int
    order_reference: str
    total_weight: int = Field(
        ..., gt=0, description="Khối lượng chuyến hàng phải lớn hơn 0"
    )
    dispatch_date: date
    shift: ShiftEnum


carriers = [
    {
        "id": 1,
        "code": "GHN",
        "name": "Giao Hang Nhanh",
        "max_weight_capacity": 5000,
        "status": "ACTIVE",
    },
    {
        "id": 2,
        "code": "GHTK",
        "name": "Giao Hang Tiet Kiem",
        "max_weight_capacity": 3000,
        "status": "ACTIVE",
    },
    {
        "id": 3,
        "code": "VTP",
        "name": "Viettel Post",
        "max_weight_capacity": 10000,
        "status": "SUSPENDED",
    },
]

shipments = [
    {
        "id": 1,
        "carrier_id": 1,
        "order_reference": "ORD-2026-001",
        "total_weight": 4200,
        "dispatch_date": date(2026, 7, 1),
        "shift": "MORNING",
    }
]

carrier_id_counter = 4
shipment_id_counter = 2


@app.post("/carriers", status_code=status.HTTP_201_CREATED)
def create_carrier(carrier_in: CarrierCreate):
    global carrier_id_counter
    if any(c["code"].upper() == carrier_in.code.upper() for c in carriers):
        raise HTTPException(status_code=400, detail="Carrier code already exists.")

    new_carrier = {
        "id": carrier_id_counter,
        "code": carrier_in.code,
        "name": carrier_in.name,
        "max_weight_capacity": carrier_in.max_weight_capacity,
        "status": carrier_in.status.value,
    }
    carriers.append(new_carrier)
    carrier_id_counter += 1
    return new_carrier


@app.get("/carriers")
def get_carriers(
    keyword: Optional[str] = Query(
        None, description="Tìm không phân biệt chữ hoa/thường theo code hoặc name"
    ),
    status: Optional[CarrierStatus] = Query(
        None, description="Lọc chính xác theo trạng thái"
    ),
    min_weight: Optional[int] = Query(
        None, description="Lọc tải trọng tối đa từ mức này trở lên"
    ),
):
    filtered = carriers
    if keyword:
        k = keyword.lower()
        filtered = [
            c for c in filtered if k in c["name"].lower() or k in c["code"].lower()
        ]
    if status:
        filtered = [c for c in filtered if c["status"] == status.value]
    if min_weight is not None:
        filtered = [c for c in filtered if c["max_weight_capacity"] >= min_weight]
    return filtered


@app.get("/carriers/{carrier_id}")
def get_carrier(carrier_id: int):
    carrier = next((c for c in carriers if c["id"] == carrier_id), None)
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")
    return carrier


@app.put("/carriers/{carrier_id}")
def update_carrier(carrier_id: int, carrier_in: CarrierUpdate):
    carrier = next((c for c in carriers if c["id"] == carrier_id), None)
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")

    if carrier_in.name is not None:
        carrier["name"] = carrier_in.name
    if carrier_in.max_weight_capacity is not None:
        carrier["max_weight_capacity"] = carrier_in.max_weight_capacity
    if carrier_in.status is not None:
        carrier["status"] = carrier_in.status.value
    return carrier


@app.delete("/carriers/{carrier_id}")
def delete_carrier(carrier_id: int):
    global carriers
    carrier = next((c for c in carriers if c["id"] == carrier_id), None)
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")

    carriers = [c for c in carriers if c["id"] != carrier_id]
    return {"message": "Carrier deleted successfully"}


@app.post("/shipments", status_code=status.HTTP_201_CREATED)
def create_shipment(shipment_in: ShipmentCreate):
    global shipment_id_counter

    carrier = next((c for c in carriers if c["id"] == shipment_in.carrier_id), None)
    if not carrier:
        raise HTTPException(status_code=400, detail="Carrier ID does not exist.")
    if carrier["status"] != "ACTIVE":
        raise HTTPException(status_code=400, detail="Selected carrier is not ACTIVE.")
    if shipment_in.total_weight > carrier["max_weight_capacity"]:
        raise HTTPException(
            status_code=400,
            detail=f"Total weight exceeds carrier's max capacity ({carrier['max_weight_capacity']}).",
        )
    is_duplicated = any(
        s["carrier_id"] == shipment_in.carrier_id
        and s["dispatch_date"] == shipment_in.dispatch_date
        and s["shift"] == shipment_in.shift.value
        for s in shipments
    )
    if is_duplicated:
        raise HTTPException(
            status_code=400,
            detail="This carrier is already scheduled for another shipment on this date and shift.",
        )

    new_shipment = {
        "id": shipment_id_counter,
        "carrier_id": shipment_in.carrier_id,
        "order_reference": shipment_in.order_reference,
        "total_weight": shipment_in.total_weight,
        "dispatch_date": shipment_in.dispatch_date,
        "shift": shipment_in.shift.value,
    }
    shipments.append(new_shipment)
    shipment_id_counter += 1
    return new_shipment


@app.get("/shipments")
def get_shipments():
    return shipments