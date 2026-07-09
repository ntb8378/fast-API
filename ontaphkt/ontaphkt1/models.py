from database import base
from sqlalchemy import Column, Integer, String

class Book(base):
    __tablename__ = "book"
    
    id = Column(Integer , primary_key= True , nullable= False, autoincrement=True)
    title = Column(String(255) , nullable= False)
    author = Column(String(255) , nullable= False)
    isbn = Column(String(255) , unique=True , nullable= False)
    status = Column(String(255) , nullable= False)

