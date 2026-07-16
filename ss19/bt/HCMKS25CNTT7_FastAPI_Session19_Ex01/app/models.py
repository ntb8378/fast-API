# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    warehouse_name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)

    # Quan hệ 1-N: Một Warehouse có nhiều Packages
    packages = relationship(
        "Package", back_populates="warehouse", cascade="all, delete-orphan"
    )


class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    package_code = Column(String(100), unique=True, nullable=False, index=True)
    weight = Column(Float, nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)

    # Quan hệ N-1 ngược về Warehouse
    warehouse = relationship("Warehouse", back_populates="packages")

    # Quan hệ 1-1 với Waybill: Cấu hình uselist=False ở phía "chủ thể"
    waybill = relationship(
        "Waybill", back_populates="package", uselist=False, cascade="all, delete-orphan"
    )


class Waybill(Base):
    __tablename__ = "waybills"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String(100), unique=True, nullable=False, index=True)
    shipping_status = Column(String(100), nullable=False)

    # Khóa ngoại ràng buộc unique=True đảm bảo tính độc bản (Quan hệ 1-1)
    package_id = Column(Integer, ForeignKey("packages.id"), unique=True, nullable=False)

    # Quan hệ 1-1 ngược về Package
    package = relationship("Package", back_populates="waybill")
