from typing import Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload
from models.classroom import Classroom
from models.student import Student
from schemas.student import StudentCreate, StudentUpdate


class BusinessError(Exception):
    def __init__(
        self, status_code: int, message: str, error_detail: Optional[str] = None
    ):
        self.status_code = status_code
        self.message = message
        self.error_detail = error_detail


class StudentService:

    @staticmethod
    def get_all(db: Session, q: Optional[str] = None, class_id: Optional[int] = None):
        query = db.query(Student).options(joinedload(Student.classroom))

        if class_id is not None:
            query = query.filter(Student.class_id == class_id)

        if q:
            search = f"%{q.strip()}%"
            query = query.filter(
                or_(
                    Student.full_name.ilike(search),
                    Student.student_code.ilike(search),
                    Student.email.ilike(search),
                )
            )

        return query.all()

    @staticmethod
    def get_by_id(db: Session, student_id: int):
        student = (
            db.query(Student)
            .options(joinedload(Student.classroom))
            .filter(Student.id == student_id)
            .first()
        )
        if not student:
            raise BusinessError(
                404, "Không tìm thấy sinh viên", f"ID {student_id} không tồn tại."
            )
        return student

    @staticmethod
    def create(db: Session, payload: StudentCreate):
        # 1. Kiểm tra lớp
        classroom = db.query(Classroom).filter(Classroom.id == payload.class_id).first()
        if not classroom:
            raise BusinessError(400, "Lớp học không tồn tại")
        if classroom.status.lower() != "active":
            raise BusinessError(400, "Lớp học không ở trạng thái hoạt động")

        # 2. Kiểm tra sĩ số
        count = db.query(Student).filter(Student.class_id == payload.class_id).count()
        if count >= classroom.max_students:
            raise BusinessError(400, "Lớp học đã đủ số lượng sinh viên")

        # 3. Kiểm tra trùng mã sinh viên & email
        if (
            db.query(Student)
            .filter(Student.student_code == payload.student_code)
            .first()
        ):
            raise BusinessError(400, "Mã sinh viên đã tồn tại")
        if db.query(Student).filter(Student.email == payload.email).first():
            raise BusinessError(400, "Email đã được sử dụng")

        new_student = Student(**payload.model_dump())
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        db.refresh(new_student, ["classroom"])
        return new_student

    @staticmethod
    def update(db: Session, student_id: int, payload: StudentUpdate):
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise BusinessError(404, "Không tìm thấy sinh viên")

        # Kiểm tra trùng lập mã & email với người khác
        if (
            db.query(Student)
            .filter(
                Student.student_code == payload.student_code, Student.id != student_id
            )
            .first()
        ):
            raise BusinessError(400, "Mã sinh viên đã bị trùng với sinh viên khác")

        if (
            db.query(Student)
            .filter(Student.email == payload.email, Student.id != student_id)
            .first()
        ):
            raise BusinessError(400, "Email đã bị trùng với sinh viên khác")

        # Kiểm tra khi chuyển lớp
        if payload.class_id != student.class_id:
            new_class = (
                db.query(Classroom).filter(Classroom.id == payload.class_id).first()
            )
            if not new_class:
                raise BusinessError(400, "Lớp học mới không tồn tại")
            if new_class.status.lower() != "active":
                raise BusinessError(400, "Lớp học mới không hoạt động")

            target_count = (
                db.query(Student).filter(Student.class_id == payload.class_id).count()
            )
            if target_count >= new_class.max_students:
                raise BusinessError(400, "Lớp học mới đã đầy")

        for key, value in payload.model_dump().items():
            setattr(student, key, value)

        db.commit()
        db.refresh(student)
        db.refresh(student, ["classroom"])
        return student
