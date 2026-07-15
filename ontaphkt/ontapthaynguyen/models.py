from sqlalchemy import Column, String, Float, Integer
from database import Base

class DeviceModel(Base):
    __tablename__ ="Device"

    id = Column(String(255), primary_key=True, unique=True)
    category = Column(String(255), nullable=False)
    model= Column(String(255), nullable=False)
    rental_rate = Column(Float , nullable=False)
    release_year = Column(Integer , nullable=False)
    status= Column(String(55), nullable=False, default="available")

