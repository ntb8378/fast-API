#thiet lap model cho students
from database import Base
from sqlalchemy import Column,Integer,String

class StudentModel(Base):
    __tablename__ = "students"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    fullname = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        nullable=False,
        unique=True,
        index=True
    )