from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL ="mysql+pymysql://thienbao:123456$@localhost:3306/user_db"

engine = create_engine(url = DATABASE_URL, pool_size=10)

LocalSession = sessionmaker(bind=engine , autoflush= False , autocommit= False)

class BASE(DeclarativeBase):
    pass
BASE.metadata.create_all(bind= engine)

def get_db():
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()