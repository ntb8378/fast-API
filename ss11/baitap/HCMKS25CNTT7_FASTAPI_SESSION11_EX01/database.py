"""Kết nối"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import pymysql

SQLACHEMY_DATABASE_URL = "mysql+pymysql://root:12345678@localhost:3306/parking_db"

temp_conn = pymysql.connect(host="localhost", user="root", password="12345678")
try:
    with temp_conn.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS parking_db")
finally:
    temp_conn.close()

engine = create_engine(
    SQLACHEMY_DATABASE_URL, pool_pre_ping=True  # Tự động kiểm tra nếu mách ngắt
)

SESSIONLOCAL = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Lấy"""
    db = SESSIONLOCAL()
    try:
        yield db
    finally:
        db.close()
