from app.db.database import Base
from sqlalchemy import Column, Integer, String

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    