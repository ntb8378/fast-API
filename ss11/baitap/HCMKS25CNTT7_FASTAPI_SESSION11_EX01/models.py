"""Cấu trúc table"""

from sqlalchemy import Boolean, Column, Integer, String
from database import Base


class ParkingSlot(Base):
    """Cấu hình bảng"""

    __tablename__ = "parking_slots"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    slot_code = Column(String(50), nullable=False, unique=True)
    zone_name = Column(String(255), nullable=False)
    max_weight = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)
