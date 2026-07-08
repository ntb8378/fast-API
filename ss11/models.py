from database import Base
from sqlalchemy import Column, Integer, String, Boolean
class ParkingModel(Base):
    __tablename__ = "parking_slots"
    id = Column(Integer, primary_key=True , autoincrement=True)
    slot_code = Column(String(50), nullable=False, unique=True)
    zone_name = Column(String(255),nullable=False)
    max_weight = Column(Integer,nullable=False)
    is_available = Column(Boolean,default=1)
class ParkingDTO(Base):
    id : int
    slot_code : str
    zone_name : str
    max_weight : int
    is_available : Boolean