from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError

from database import Base, engine
from routers import student_router
from schemas.response import response_format
from services.student_service import BusinessError

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Quản lý Sinh viên")


# Handlers xử lý lỗi toàn cục
@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError):
    return response_format(
        request, exc.status_code, exc.message, error=exc.error_detail
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = [
        {
            "field": " -> ".join([str(p) for p in e["loc"] if p != "body"]),
            "issue": e["msg"],
        }
        for e in exc.errors()
    ]
    return response_format(
        request,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "Dữ liệu đầu vào không hợp lệ",
        error=errors,
    )


# Đăng ký các API Routers
app.include_router(student_router.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
