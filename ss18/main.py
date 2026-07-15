from fastapi import FastAPI
from database import Base, engine, get_db
from app.models.student_model import StudentModel
from app.routers.student_router import student_router

app = FastAPI(
    title="Student API"
)

Base.metadata.create_all(bind = engine)

app.include_router(student_router)


@app.get("/")
def get_root():
    return "Server đang khởi chạy"