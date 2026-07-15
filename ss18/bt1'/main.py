from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import schemas
import crud

# Khởi tạo database tables khi chạy ứng dụng
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Department Employee Management API")


@app.post(
    "/departments",
    response_model=schemas.DepartmentDetailResponse,  # Mặc định trả về thông tin phòng ban trống nhân viên
    status_code=status.HTTP_201_CREATED,
)
def api_create_department(
    data: schemas.DepartmentCreate, db: Session = Depends(get_db)
):
    return crud.create_department(db=db, data=data)


@app.get(
    "/departments/{department_id}", response_model=schemas.DepartmentDetailResponse
)
def api_get_department_detail(department_id: int, db: Session = Depends(get_db)):
    return crud.get_department_by_id(db=db, department_id=department_id)


@app.post(
    "/employees",
    response_model=schemas.EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def api_create_employee(data: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db=db, data=data)
