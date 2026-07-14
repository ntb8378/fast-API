from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://thienbao:123456$@localhost:3306/student_db"

Base = declarative_base()

engine = create_engine(DATABASE_URL)

LocalSession = sessionmaker(
    bind = engine,
    autoflush= False,
    autocommit = False
)

def get_db():
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()