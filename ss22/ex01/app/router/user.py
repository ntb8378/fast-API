from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
import app.service.user as service_user
from app.db.database import get_db


router = APIRouter(
prefix= "/api/users",
tags=["Authentication"]
)
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    data = service_user.create_user(db, user)
    return {
    "status_code": 201,
    "message": "Tạo thành công",
    "data": data
    }

