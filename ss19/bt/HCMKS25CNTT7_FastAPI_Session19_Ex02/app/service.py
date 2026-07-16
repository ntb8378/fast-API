from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException, status


# 1. Nghiệp vụ: Tạo mới Phòng khám
def create_clinic(db: Session, clinic_in: schemas.ClinicCreate):
    db_clinic = models.Clinic(**clinic_in.model_dump())
    try:
        db.add(db_clinic)
        db.commit()
        db.refresh(db_clinic)
        return db_clinic
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi hệ thống khi tạo phòng khám: {str(e)}",
        )


# 2. Nghiệp vụ: Lấy chi tiết Phòng khám
def get_clinic_by_id(db: Session, clinic_id: int):
    # Dữ liệu quan hệ (doctors) sẽ được tự động nạp qua thuộc tính relationship()
    db_clinic = db.query(models.Clinic).filter(models.Clinic.id == clinic_id).first()
    if not db_clinic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy Phòng khám với ID {clinic_id}",
        )
    return db_clinic


# 3. Nghiệp vụ: Cập nhật động PATCH thông tin Bác sĩ
def update_doctor(db: Session, doctor_id: int, doctor_in: schemas.DoctorUpdate):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy Bác sĩ với ID {doctor_id}",
        )

    # model_dump(exclude_unset=True) giúp loại bỏ các trường người dùng không truyền lên
    update_data = doctor_in.model_dump(exclude_unset=True)

    try:
        for key, value in update_data.items():
            setattr(db_doctor, key, value)

        db.commit()
        db.refresh(db_doctor)
        return db_doctor
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi hệ thống khi cập nhật bác sĩ: {str(e)}",
        )


# 4. Nghiệp vụ: Xóa vĩnh viễn (Hard Delete) Chứng chỉ hành nghề
def delete_license(db: Session, license_id: int):
    db_license = (
        db.query(models.License).filter(models.License.id == license_id).first()
    )
    if not db_license:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy Chứng chỉ hành nghề với ID {license_id}",
        )

    try:
        db.delete(db_license)
        db.commit()
        return {
            "message": f"Đã xóa vĩnh viễn chứng chỉ hành nghề có ID {license_id} thành công"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi hệ thống khi xóa chứng chỉ: {str(e)}",
        )
