from app. schemas.user import UserCreate
from sqlalchemy.orm import Session
from app.models.user import UserModel
from fastapi import HTTPException
from app.cores.security import hash_password

def create_user(db: Session, user: UserCreate):
    exit_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if exit_user:
        raise HTTPException(
            status_code=400,
            detail="đã tồn tại!"
        )
    hashed_password = hash_password(user.password)
    new_user = UserModel(
        username = user.username,
        hash_password = hash_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user