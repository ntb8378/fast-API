# app/main.py
from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app import schemas, service

# Khởi tạo bảng tự động trong MySQL (Tiện ích môi trường Dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Supply Chain Management API System",
    description="Hệ thống quản lý chuỗi cung ứng chuẩn hóa quan hệ 1-N và 1-1.",
    version="1.0.0",
)


@app.post(
    "/warehouses",
    response_model=schemas.WarehouseDetailResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Warehouses"],
)
def api_create_warehouse(
    warehouse_in: schemas.WarehouseCreate, db: Session = Depends(get_db)
):
    """Tạo mới một Nhà kho lưu trữ dữ liệu."""
    return service.create_warehouse(db=db, warehouse_in=warehouse_in)


@app.get(
    "/warehouses/{warehouse_id}",
    response_model=schemas.WarehouseDetailResponse,
    status_code=status.HTTP_200_OK,
    tags=["Warehouses"],
)
def api_get_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    """Truy vấn thông tin chi tiết Nhà kho kèm theo danh sách Kiện hàng trực thuộc."""
    return service.get_warehouse_by_id(db=db, warehouse_id=warehouse_id)


@app.patch(
    "/packages/{package_id}",
    response_model=schemas.PackageResponse,
    status_code=status.HTTP_200_OK,
    tags=["Packages"],
)
def api_update_package(
    package_id: int, package_in: schemas.PackageUpdate, db: Session = Depends(get_db)
):
    """Cập nhật động các thông tin tùy chọn của một Kiện hàng cụ thể (PATCH)."""
    return service.update_package(db=db, package_id=package_id, package_in=package_in)


@app.delete("/waybills/{waybill_id}", status_code=status.HTTP_200_OK, tags=["Waybills"])
def api_delete_waybill(waybill_id: int, db: Session = Depends(get_db)):
    """Xóa vật lý (Hard Delete) hoàn toàn Vận đơn chi tiết ra khỏi Hệ thống."""
    return service.delete_waybill(db=db, waybill_id=waybill_id)
