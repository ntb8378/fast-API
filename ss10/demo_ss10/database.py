# Cau hinh ket noi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#1. Dinh nghia chuoi ket noi (connection string)
DATABASE_URL = "mysql+pymysql://thienbao:123456$@localhost/school_db"

#2. kho tao doi tuong Engine quan lys Connection Pool

engine = create_engine(DATABASE_URL)

#3. Khoi tao Factory session local dung de sinh ra session

SessionLocal = sessionmaker(
    autoflush=False, #ngăn chặn quá trình tự động cập nhật các thay đổi tạm thời trước khi các câu lệnh query đc khởi tạo
    bind=engine,
    autocommit = False
)

#khai báo base class định nghĩa các model
Base = declarative_base()

# Genenator Function quản lý vòng đời của database session
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()