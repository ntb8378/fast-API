# pyrefly: ignore [missing-import]
from sqlalchemy import Column, String, Integer, ForeignKey, Table
# pyrefly: ignore [missing-import]
from database import Base
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship

# Bảng trung gian
student_course = Table(
    "student_courses",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)

class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))

    # Liên kết theo mối quan hệ 1 - 1
    # Liên kết mối quan hệ theo chiêu xuôi
    profile = relationship("ProfileModel", back_populates="student", uselist=False)
    department = relationship("DepartmentModel", back_populates="students")
    courses = relationship("CourseModel", secondary=student_course, back_populates="students")


class ProfileModel(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bio = Column(String(100))
    #  Tạo khóa ngoại
    student_id = Column(Integer, ForeignKey("students.id"), unique=True)
    # Liên kết theo chiều ngược
    student = relationship("StudentModel", back_populates="profile")


# Tạo bảng Department liên kết với bảng student với mối quan hệ 1 nhiều
class DepartmentModel(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    students = relationship("StudentModel", back_populates="department")

# Tạo bảng course liên kết với bảng student với mối quan hệ nhiều nhiều
class CourseModel(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    students = relationship("StudentModel", secondary=student_course, back_populates="courses")