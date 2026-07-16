from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Clinic(Base):
    __tablename__ = "clinics"

    id = Column(Integer, primary_key=True, index=True)
    clinic_name = Column(String(255), nullable=False)
    specialty = Column(String(255), nullable=False)

    # Quan hệ 1-N: Một Clinic có nhiều Doctors
    doctors = relationship(
        "Doctor", back_populates="clinic", cascade="all, delete-orphan"
    )


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    doctor_code = Column(String(50), unique=True, nullable=False, index=True)
    salary = Column(Float, nullable=False)
    clinic_id = Column(
        Integer, ForeignKey("clinics.id", ondelete="CASCADE"), nullable=False
    )

    # Quan hệ N-1: Nhiều Bác sĩ thuộc về một Clinic
    clinic = relationship("Clinic", back_populates="doctors")

    # Quan hệ 1-1: Sử dụng uselist=False để giới hạn chỉ lấy 1 đối tượng đơn lẻ
    license = relationship(
        "License", back_populates="doctor", uselist=False, cascade="all, delete-orphan"
    )


class License(Base):
    __tablename__ = "licenses"

    id = Column(Integer, primary_key=True, index=True)
    license_number = Column(String(100), unique=True, nullable=False, index=True)
    issue_by = Column(String(255), nullable=False)
    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    # Quan hệ 1-1 đối ứng
    doctor = relationship("Doctor", back_populates="license")
