from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from models.user_course import enrollments


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_code = Column(String(20), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    class_id = Column(Integer, ForeignKey("classrooms.id"), nullable=False)

    classroom = relationship("Classroom", back_populates="students")

    # 2. Đổi "enrollments" (chuỗi) thành biến enrollments
    courses = relationship("Course", secondary=enrollments, back_populates="students")
