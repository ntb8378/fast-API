from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app import schemas, service

# Khởi tạo tự động các bảng trong database dựa trên khai báo ở models.py
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hệ thống Quản lý Y tế - Thiết kế Mô hình & API chuẩn hóa", version="1.0.0"
)


@app.post(
    "/clinics",
    response_model=schemas.ClinicDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo mới một phòng khám/chuyên khoa",
)
def create_clinic_endpoint(
    clinic_in: schemas.ClinicCreate, db: Session = Depends(get_db)
):
    return service.create_clinic(db=db, clinic_in=clinic_in)


@app.get(
    "/clinics/{clinic_id}",
    response_model=schemas.ClinicDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy thông tin chi tiết phòng khám và danh sách bác sĩ trực thuộc",
)
def get_clinic_endpoint(clinic_id: int, db: Session = Depends(get_db)):
    return service.get_clinic_by_id(db=db, clinic_id=clinic_id)


@app.patch(
    "/doctors/{doctor_id}",
    status_code=status.HTTP_200_OK,
    summary="Cập nhật động (PATCH) thông tin của Bác sĩ",
)
def update_doctor_endpoint(
    doctor_id: int, doctor_in: schemas.DoctorUpdate, db: Session = Depends(get_db)
):
    # Trả về đối tượng Doctor sau cập nhật
    updated_doctor = service.update_doctor(
        db=db, doctor_id=doctor_id, doctor_in=doctor_in
    )
    return {
        "message": "Cập nhật thông tin bác sĩ thành công",
        "doctor": {
            "id": updated_doctor.id,
            "doctor_code": updated_doctor.doctor_code,
            "salary": updated_doctor.salary,
            "clinic_id": updated_doctor.clinic_id,
        },
    }


@app.delete(
    "/licenses/{license_id}",
    status_code=status.HTTP_200_OK,
    summary="Xóa vĩnh viễn (Hard Delete) chứng chỉ hành nghề",
)
def delete_license_endpoint(license_id: int, db: Session = Depends(get_db)):
    return service.delete_license(db=db, license_id=license_id)
