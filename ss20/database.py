from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://thienbao:123456$@localhost:3306/ss20_db"

temp_conn = pymysql.connect(host="localhost", user="thienbao", password="123456$")

try:
    with temp_conn.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ss20_db")
finally:
    temp_conn.close()

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
