# app/service.py
from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException, status


# --- WAREHOUSE SERVICES ---
def create_warehouse(db: Session, warehouse_in: schemas.WarehouseCreate):
    db_warehouse = models.Warehouse(**warehouse_in.model_dump())
    try:
        db.add(db_warehouse)
        db.commit()
        db.refresh(db_warehouse)
        return db_warehouse
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi hệ thống khi tạo nhà kho: {str(e)}",
        )


def get_warehouse_by_id(db: Session, warehouse_id: int):
    # Sử dụng thuộc tính lười (Lazy Loading mặc định hoặc Eager Loading) để tự gom quan hệ
    db_warehouse = (
        db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()
    )
    if not db_warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy Nhà kho với ID {warehouse_id}",
        )
    return db_warehouse


# --- PACKAGE SERVICES ---
def update_package(db: Session, package_id: int, package_in: schemas.PackageUpdate):
    db_package = (
        db.query(models.Package).filter(models.Package.id == package_id).first()
    )
    if not db_package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy Kiện hàng với ID {package_id}",
        )

    # Lấy các trường thực sự truyền lên từ Client
    update_data = package_in.model_dump(exclude_unset=True)

    try:
        for key, value in update_data.items():
            setattr(db_package, key, value)

        db.commit()
        db.refresh(db_package)
        return db_package
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi hệ thống khi cập nhật kiện hàng: {str(e)}",
        )


# --- WAYBILL SERVICES ---
def delete_waybill(db: Session, waybill_id: int):
    db_waybill = (
        db.query(models.Waybill).filter(models.Waybill.id == waybill_id).first()
    )
    if not db_waybill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy Vận đơn với ID {waybill_id}",
        )

    try:
        db.delete(db_waybill)  # Hard Delete vật lý
        db.commit()
        return {"message": f"Xóa thành công vận đơn có ID {waybill_id} khỏi hệ thống"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi hệ thống khi xóa vận đơn: {str(e)}",
        )
