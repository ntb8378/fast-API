# Tạo hàm thêm dữ liệu
from sqlalchemy.orm import Session
from schemas import UsersRequestDTO
from models import UsersModel
from fastapi import HTTPException

def create_user(db: Session, user: UsersRequestDTO):
    try:
        new_user = UsersModel(
            name = user.name,
            email = user.email
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        # quay lại và thoát ra không lưu
        raise HTTPException(status_code=400, detail=f"Lỗi trong quá trình thêm {str(e)}")

# Lấy ra user
def get_user(db: Session, user_id: int):
    return db.query(UsersModel).filter(UsersModel.id == user_id).first()
