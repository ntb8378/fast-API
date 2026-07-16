from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Thay đổi thông tin user, password, host, port và db_name phù hợp với môi trường của bạn
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/medical_db"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Tự động kiểm tra trạng thái kết nối
    pool_recycle=3600,  # Tự động giải phóng kết nối sau 1 giờ
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency để inject vào các API endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
