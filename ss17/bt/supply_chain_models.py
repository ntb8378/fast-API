from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


# ==========================
# Association Table
# ==========================
package_truck = Table(
    "package_truck",
    Base.metadata,
    Column("package_id", Integer, ForeignKey("packages.id"), primary_key=True),
    Column("truck_id", Integer, ForeignKey("trucks.id"), primary_key=True),
)


# ==========================
# Warehouse
# ==========================
class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    warehouse_name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)

    packages = relationship("Package", back_populates="warehouse")


# ==========================
# Package
# ==========================
class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_code = Column(String(100), unique=True, nullable=False)
    weight = Column(Float, nullable=False)

    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)

    warehouse = relationship("Warehouse", back_populates="packages")

    waybill = relationship(
        "Waybill",
        back_populates="package",
        uselist=False
    )

    trucks = relationship(
        "Truck",
        secondary=package_truck,
        back_populates="packages"
    )


# ==========================
# Waybill
# ==========================
class Waybill(Base):
    __tablename__ = "waybills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tracking_number = Column(String(100), nullable=False)
    shipping_status = Column(String(100), nullable=False)

    package_id = Column(
        Integer,
        ForeignKey("packages.id"),
        unique=True,
        nullable=False
    )

    package = relationship("Package", back_populates="waybill")


# ==========================
# Truck
# ==========================
class Truck(Base):
    __tablename__ = "trucks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    license_plate = Column(String(100), nullable=False)

    packages = relationship(
        "Package",
        secondary=package_truck,
        back_populates="trucks"
    )