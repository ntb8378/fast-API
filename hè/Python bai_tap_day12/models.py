from database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author_id = Column(Integer,ForeignKey("authors.id"), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    borrow_count = Column(Integer, default=0)
    available_quantity = Column(Integer, default=0)

    author = relationship("AuthorModel", back_populates="books")

class AuthorModel(Base):
    __tablename__ = "authors"
    id = Column(int, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    bio = Column(String(255), nullable=False)

    books = relationship("BookModel", back_populates="author")