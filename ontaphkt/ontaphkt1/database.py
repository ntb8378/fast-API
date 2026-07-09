from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://thienbao:123456$@localhost:3306/book_db"

engine = create_engine(DATABASE_URL)

LocalSession = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():
    try:
        db= LocalSession()
        yield db
    finally:
        db.close()

base = declarative_base()
