from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db, Base, engine
from models import UsersModel
from schemas import UsersRequestDTO
from user_services import create_user, get_user
# import user_services
app = FastAPI(
    title="Manager User"
)

Base.metadata.create_all(bind= engine)

@app.get("/test")
def test(db:Session = Depends(get_db)):
    try:
        db.execute(text('SELECT 1'))
        return{
            "message": "kết nối thành công!"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"kết nối thất bại{str(e)}")
    

# API thêm user
@app.post("/users", tags=["Users"])
def add_users(user:UsersRequestDTO , db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=400, detail="thêm không thành công!")
    return {
        "status_code": 200,
        "message": "thêm thành công",
        "data": db_user
    }

# API lấy user
@app.get("/users/{user_id}", tags=["Users"])
def det_users(user_id:int ,db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="ID NOT FOUND")
    
    return {
        "status_code": 200,
        "message": "lấy thông tin thành công!",
        "data": db_user
    }