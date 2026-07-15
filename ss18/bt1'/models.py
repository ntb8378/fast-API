from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False)
    max_employees = Column(Integer, nullable=False)

    # Quan hệ 1-Nhiều: Một phòng ban có nhiều nhân viên
    employees = relationship("Employee", back_populates="department")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(
        String(20), nullable=False, unique=True
    )  # Đảm bảo duy nhất tầng DB
    full_name = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)

    # Quan hệ Nhiều-1: Một nhân viên chỉ thuộc về một phòng ban
    department = relationship("Department", back_populates="employees")
