from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Classroom(Base):
    __tablename__ = "classrooms"
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_code = Column(String(20), nullable=False, unique=True)
    class_name = Column(String(100), nullable=False)
    max_students = Column(Integer, default=30, nullable=False)
    status = Column(String(20), default="active", nullable=False)

    students = relationship("Student", back_populates="classroom")
