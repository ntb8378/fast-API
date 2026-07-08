from datetime import datetime, timezone

import models
from database import engine, get_db
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from schemas import (
    ParkingSlotCreate,
    ParkingSlotResponseData,
    StandarResponse,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Quản lý Vị trí Xe Công nghệ")


def make_response(
    status_code: int, message: str, data: any, path: str, error: str = None
):
    """Cấu trúc reponse"""
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post(
    "/parking-slots",
    response_model=StandarResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_parking_slot(
    request: Request, slot_data: ParkingSlotCreate, db: Session = Depends(get_db)
):
    """Thêm vị trí đỗ xe mới"""
    db_slot = models.ParkingSlot(
        slot_code=slot_data.slot_code,
        zone_name=slot_data.zone_name,
        max_weight=slot_data.max_weight,
        is_available=slot_data.is_available,
    )

    try:
        db.add(db_slot)
        db.commit()
        db.refresh(db_slot)

        response_data = ParkingSlotResponseData.model_validate(db_slot).model_dump()
        return make_response(
            status_code=201,
            message="Thêm vị trí thành công",
            data=response_data,
            path=str(request.url.path),
        )

    except IntegrityError:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=make_response(
                status_code=400,
                message="Mã vị trí đỗ xe (slot_code) đã tồn tại trên hệ thống",
                error="Bad Request",
                data=None,
                path=str(request.url.path),
            ),
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=make_response(
                status_code=500,
                message="Lỗi hệ thống không xác định",
                error=str(e),
                data=None,
                path=str(request.url.path),
            ),
        )


@app.get("/parking-slots", response_model=StandarResponse)
def get_all_parking_slots(reqest: Request, db: Session = Depends(get_db)):
    """Lấy danh sách vị trí đỗ"""
    slots = db.query(models.ParkingSlot).all()

    response_data = [
        ParkingSlotResponseData.model_validate(slot).model_dump() for slot in slots
    ]

    return make_response(
        status_code=200,
        message="Lấy danh sách vị trí đỗ xe thành công",
        data=response_data,
        path=str(reqest.url.path),
    )


@app.get("/parking-slots/{slot_id}", response_model=StandarResponse)
def get_parking_slot_detail(
    slot_id: int, request: Request, db: Session = Depends(get_db)
):
    """Lấy chi tiết theo 1 vị trí đỗ"""
    slot = db.query(models.ParkingSlot).filter(models.ParkingSlot.id == slot_id).first()

    if not slot:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=make_response(
                status_code=404,
                message="Parking slot not found",
                error="Not Found",
                data=None,
                path=str(request.url.path),
            ),
        )

    response_data = ParkingSlotResponseData.model_validate(slot).model_dump()
    return make_response(
        status_code=200,
        message="Lấy thông tin chi tiết thành công",
        data=response_data,
        path=str(request.url.path),
    )
