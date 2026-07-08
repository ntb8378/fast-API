from database import Base
from sqlalchemy import Column , Integer , String , Boolean

class UsersModel(Base):
    __tablename__ = "users"

    id = Column(Integer , primary_key= True , index= True, autoincrement= True)
    name = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)