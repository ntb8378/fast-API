from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://thienbao:123456$@localhost:3306/ss11_db"

engine = create_engine(DATABASE_URL)

session = sessionmaker(bind = engine , autocommit = False , autoflush= False)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
Base = declarative_base()