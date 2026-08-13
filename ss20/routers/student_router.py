from typing import Optional
from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.response import response_format
from schemas.student import StudentCreate, StudentResponse, StudentUpdate
from services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("", status_code=status.HTTP_200_OK)
def get_students(
    request: Request,
    q: Optional[str] = Query(None, description="Tìm theo tên, mã SV, email"),
    class_id: Optional[int] = Query(None, ge=1),
    db: Session = Depends(get_db),
):
    students = StudentService.get_all(db, q, class_id)
    data = [StudentResponse.model_validate(s).model_dump() for s in students]
    return response_format(
        request, 200, "Lấy danh sách sinh viên thành công", data=data
    )


@router.get("/{student_id}", status_code=status.HTTP_200_OK)
def get_student(student_id: int, request: Request, db: Session = Depends(get_db)):
    student = StudentService.get_by_id(db, student_id)
    data = StudentResponse.model_validate(student).model_dump()
    return response_format(
        request, 200, "Lấy thông tin sinh viên thành công", data=data
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_student(
    payload: StudentCreate, request: Request, db: Session = Depends(get_db)
):
    student = StudentService.create(db, payload)
    data = StudentResponse.model_validate(student).model_dump()
    return response_format(request, 201, "Thêm mới sinh viên thành công", data=data)


@router.put("/{student_id}", status_code=status.HTTP_200_OK)
def update_student(
    student_id: int,
    payload: StudentUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    student = StudentService.update(db, student_id, payload)
    data = StudentResponse.model_validate(student).model_dump()
    return response_format(request, 200, "Cập nhật sinh viên thành công", data=data)
