from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import models
import schemas


# TẠO PHÒNG BAN
def create_department(db: Session, data: schemas.DepartmentCreate):
    db_department = models.Department(
        name=data.name, status=data.status, max_employees=data.max_employees
    )
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


# LẤY CHI TIẾT PHÒNG BAN (Kèm danh sách nhân viên)
def get_department_by_id(db: Session, department_id: int):
    department = (
        db.query(models.Department)
        .filter(models.Department.id == department_id)
        .first()
    )
    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Phòng ban không tồn tại"
        )
    return department


# TẠO NHÂN VIÊN (Chứa đầy đủ các logic kiểm tra nghiêm ngặt)
def create_employee(db: Session, data: schemas.EmployeeCreate):
    # 1. Kiểm tra phòng ban có tồn tại hay không
    department = (
        db.query(models.Department)
        .filter(models.Department.id == data.department_id)
        .first()
    )
    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Phòng ban không tồn tại"
        )

    # 2. Kiểm tra trạng thái phòng ban
    if department.status == "INACTIVE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phòng ban đã ngừng hoạt động",
        )

    # 3. Kiểm tra số lượng nhân viên hiện tại (Chặn khi >= max_employees)
    current_count = (
        db.query(models.Employee)
        .filter(models.Employee.department_id == data.department_id)
        .count()
    )
    if current_count >= department.max_employees:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phòng ban đã đủ số lượng nhân viên",
        )

    # 4. Kiểm tra mã nhân viên trùng lặp trên TOÀN BỘ hệ thống
    duplicate_employee = (
        db.query(models.Employee)
        .filter(models.Employee.employee_code == data.employee_code)
        .first()
    )
    if duplicate_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã nhân viên đã tồn tại trên hệ thống",
        )

    # 5. Lưu vào Database nếu hợp lệ
    db_employee = models.Employee(
        employee_code=data.employee_code,
        full_name=data.full_name,
        department_id=data.department_id,
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee
