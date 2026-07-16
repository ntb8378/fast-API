# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Thay đổi thông tin kết nối MySQL phù hợp với môi trường của bạn
DATABASE_URL = "mysql+pymysql://root:password12345678@localhost:3306/supply_chain_db"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Kiểm tra trạng thái kết nối trước khi dùng
    pool_recycle=3600,  # Tự động đóng kết nối cũ sau 1 giờ
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency cung cấp DB Session cho các HTTP Requests
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
