from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Định dạng URL kết nối MySQL: mysql+pymysql://user:password@host:port/db_name
# Thay đổi các thông số cho phù hợp với cơ sở dữ liệu của bạn
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/pet_boarding_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True  # Tự động kiểm tra trạng thái kết nối
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
