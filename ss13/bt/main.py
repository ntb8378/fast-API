from fastapi import FastAPI, Depends, Request, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from database import SessionLocal, engine, Base
from models import BoardingSlot
import schemas

# Tự động tạo bảng nếu chưa tồn tại trong MySQL
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pet Boarding Slots API")


# Dependency lấy Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Hàm tiện ích chuẩn hóa phản hồi 6 trường
def make_response(
    status_code: int, message: str, path: str, data: any = None, error: str = None
):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


# --- 1. POST: THÊM KHOANG LƯU TRÚ MỚI ---
@app.post(
    "/boarding-slots",
    response_model=schemas.UnifiedResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_boarding_slot(
    request: Request, slot_in: schemas.BoardingSlotCreate, db: Session = Depends(get_db)
):
    db_slot = BoardingSlot(**slot_in.model_dump())
    try:
        db.add(db_slot)
        db.commit()
        db.refresh(db_slot)

        data_res = schemas.BoardingSlotResponseData.model_validate(db_slot).model_dump()
        return make_response(
            201, "Thêm khoang lưu trú mới thành công", request.url.path, data=data_res
        )

    except IntegrityError:
        db.rollback()
        return make_response(
            400, "Slot number already exists", request.url.path, error="Bad Request"
        )
    except Exception as e:
        db.rollback()
        return make_response(
            500, "Lỗi hệ thống khi thêm khoang lưu trú", request.url.path, error=str(e)
        )


# --- 2. GET: LẤY DANH SÁCH TẤT CẢ KHOANG LƯU TRÚ ---
@app.get("/boarding-slots", response_model=schemas.UnifiedResponse)
def get_all_boarding_slots(request: Request, db: Session = Depends(get_db)):
    slots = db.query(BoardingSlot).all()
    data_res = [
        schemas.BoardingSlotResponseData.model_validate(s).model_dump() for s in slots
    ]
    return make_response(
        200, "Lấy danh sách thành công", request.url.path, data=data_res
    )


# --- 3. GET: LẤY CHI TIẾT MỘT KHOANG LƯU TRÚ ---
@app.get("/boarding-slots/{slot_id}", response_model=schemas.UnifiedResponse)
def get_boarding_slot_by_id(
    slot_id: int, request: Request, db: Session = Depends(get_db)
):
    slot = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
    if not slot:
        return make_response(
            404, "Boarding slot not found", request.url.path, error="Not Found"
        )

    data_res = schemas.BoardingSlotResponseData.model_validate(slot).model_dump()
    return make_response(
        200, "Lấy chi tiết khoang lưu trú thành công", request.url.path, data=data_res
    )


# --- 4. PUT: CẬP NHẬT THÔNG TIN KHOANG LƯU TRÚ ---
@app.put("/boarding-slots/{slot_id}", response_model=schemas.UnifiedResponse)
def update_boarding_slot(
    slot_id: int,
    request: Request,
    slot_in: schemas.BoardingSlotUpdate,
    db: Session = Depends(get_db),
):
    db_slot = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
    if not db_slot:
        return make_response(
            404, "Boarding slot not found", request.url.path, error="Not Found"
        )

    try:
        # Bóc tách dữ liệu và ghi đè từng thuộc tính bằng model_dump(exclude_unset=True)
        update_data = slot_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_slot, key, value)

        db.commit()
        db.refresh(db_slot)

        data_res = schemas.BoardingSlotResponseData.model_validate(db_slot).model_dump()
        return make_response(
            200,
            "Cập nhật thông tin khoang lưu trú thành công",
            request.url.path,
            data=data_res,
        )

    except IntegrityError:
        db.rollback()
        return make_response(
            400, "Slot number already exists", request.url.path, error="Bad Request"
        )
    except Exception as e:
        db.rollback()
        return make_response(
            500,
            "Lỗi hệ thống khi cập nhật khoang lưu trú",
            request.url.path,
            error=str(e),
        )


# --- 5. DELETE: XÓA KHOANG LƯU TRÚ KHỎI HỆ THỐNG ---
@app.delete("/boarding-slots/{slot_id}", response_model=schemas.UnifiedResponse)
def delete_boarding_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    db_slot = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
    if not db_slot:
        return make_response(
            404, "Boarding slot not found", request.url.path, error="Not Found"
        )

    try:
        db.delete(db_slot)
        db.commit()
        return make_response(
            200, "Xóa khoang lưu trú thành công", request.url.path, data=None
        )
    except Exception as e:
        db.rollback()
        return make_response(
            500, "Lỗi hệ thống khi xóa khoang lưu trú", request.url.path, error=str(e)
        )
