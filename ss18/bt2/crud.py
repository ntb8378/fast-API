from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import models
import schemas


def create_classroom(db: Session, data: schemas.ClassroomCreate):
    classroom = models.Classroom(
        class_name=data.class_name, status=data.status, capacity=data.capacity
    )
    db.add(classroom)
    db.commit()
    db.refresh(classroom)
    return classroom


def create_student(db: Session, data: schemas.StudentCreate):
    classroom = (
        db.query(models.Classroom)
        .filter(models.Classroom.id == data.classroom_id)
        .first()
    )
    if classroom is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lớp học không tồn tại"
        )

    if classroom.status != "OPEN":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Lớp học đã đóng"
        )

    current_count = (
        db.query(models.Student)
        .filter(models.Student.classroom_id == data.classroom_id)
        .count()
    )
    if current_count >= classroom.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Lớp học đã đủ sinh viên"
        )

    student = models.Student(
        student_code=data.student_code,
        full_name=data.full_name,
        classroom_id=data.classroom_id,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_classroom_detail(db: Session, classroom_id: int):
    classroom = (
        db.query(models.Classroom).filter(models.Classroom.id == classroom_id).first()
    )
    if classroom is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lớp học không tồn tại"
        )

    # SỬA LỖI: Chỉ lọc sinh viên thuộc về lớp học cụ thể này
    students = (
        db.query(models.Student)
        .filter(models.Student.classroom_id == classroom_id)
        .order_by(models.Student.id)
        .all()
    )

    return {
        "id": classroom.id,
        "class_name": classroom.class_name,
        "status": classroom.status,
        "capacity": classroom.capacity,
        "students": students,
    }


def transfer_student(db: Session, student_id: int, data: schemas.TransferClassRequest):
    # 1. Tìm sinh viên theo student_id
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sinh viên không tồn tại"
        )

    # 2. Tìm lớp học đích theo new_classroom_id
    target_classroom = (
        db.query(models.Classroom)
        .filter(models.Classroom.id == data.new_classroom_id)
        .first()
    )
    if target_classroom is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lớp học đích không tồn tại"
        )

    # 3. Kiểm tra trạng thái lớp đích
    if target_classroom.status == "CLOSED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không thể chuyển sinh viên vào lớp đã đóng",
        )

    # 4. Đếm số sinh viên hiện tại của lớp đích và kiểm tra sức chứa (SỬA LỖI từ > thành >=)
    current_count = (
        db.query(models.Student)
        .filter(models.Student.classroom_id == data.new_classroom_id)
        .count()
    )
    if current_count >= target_classroom.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lớp học đích đã đủ số lượng sinh viên",
        )

    # 5. Tiến hành cập nhật
    student.classroom_id = data.new_classroom_id
    db.commit()
    db.refresh(student)
    return student
