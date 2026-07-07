from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


database_url = "mysql+pymysql://thienbao:123456$@localhost:3306/ss10_db"
engine = create_engine(database_url)
session_local = sessionmaker(autoflush=False , bind= engine , autocommit = False)

base = declarative_base

def get_db():
    db = session_local()
    try:
        yield db

    finally:
        db.close()