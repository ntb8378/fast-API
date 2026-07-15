from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://thienbao:123456$@localhost:3306/student_db"

engine = create_engine(DATABASE_URL)

LocalSession = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind = engine
)

Base = declarative_base()

def get_db():
    try:
        db  = LocalSession()
        yield db
    finally:
        db.close()