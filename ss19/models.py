from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Warehouse(Base):
    __tablename__ = "warehouse"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Warehouse_name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    package = relationship("Package", back_populates="warehouse")

class Package(Base):
    tablename_ = "packages"
    id = Column(Integer,primary_key=True,autoincrement=True)
    package_code = Column(String(255), nullable=False, unique=True)
    weight = Column(Float, nullable=False)
    warehouse_id = Column(Integer,ForeignKey("warehouses. id"),nullable=False)
    warehouse = relationship("Warehouse", back_populates="packages")
    waybill = relationship("waybill", back_populates="packages")

class Waybill(Base):
    __tablename__= "waybills"
    id = Column(Integer,primary_key=True,autoincrement=True)
    tracking_number = Column(String(255), nullable=False,unique=True)
    shipping_status = Column(String(255), nullable=False)
    package_id = Column(Integer, ForeignKey("packages.id"), unique= True, nullable= False)
    package = relationship("Package", back_populates="waybills", uselist=False)

