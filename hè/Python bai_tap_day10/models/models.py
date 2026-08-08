from database import Base
from sqlalchemy import Column, Integer, String , Float 

class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True) 
    title = Column(String(255), nullable=False) 
    author = Column(String(100), nullable=False)
    price = Column(Float, nullable=False) 
    quantity = Column(Integer, default=0) 
