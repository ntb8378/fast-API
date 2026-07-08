"""

STT	|Hành vi lỗi trong code hiện tại	|Hậu quả đối với Database MySQL	|Cách khắc phục bằng SQLAlchemy
1	|Thiếu lệnh xác thực lưu dữ liệu (db.commit())	|Bản ghi chỉ nằm trong bộ nhớ session, không được ghi xuống bảng products → Database trống rỗng	|Sau khi db.add(new_product), cần gọi db.commit() để flush và commit transaction
2	|Không giải phóng/đóng Session (db.close())	|Kết nối vẫn treo trong connection pool, lâu dài gây rò rỉ tài nguyên, nghẽn kết nối	|Dùng try/finally hoặc context manager để đảm bảo db.close() luôn được gọi sau khi hoàn tất

"""

from fastapi import FastAPI, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/ecommerce_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)


class ProductCreate(BaseModel):
    sku: str
    name: str
    price: float


app = FastAPI()


# @app.post("/products")
# def create_product(product: ProductCreate):
#     db = SessionLocal()  # Mở kết nối MySQL

#     new_product = ProductModel(sku=product.sku, name=product.name, price=product.price)
#     db.add(new_product)  # Thêm vào session

#     return {
#         "message": "Product prepared successfully",
#         "data": {"sku": product.sku, "name": product.name},
#     }


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    db = SessionLocal()
    try:
        new_product = ProductModel(
            sku=product.sku, name=product.name, price=product.price
        )
        db.add(new_product)
        db.commit()  # Ghi dữ liệu xuống DB
        db.refresh(new_product)  # Cập nhật đối tượng với ID mới
        return {
            "message": "Product created successfully",
            "data": {
                "id": new_product.id,
                "sku": new_product.sku,
                "name": new_product.name,
            },
        }
    finally:
        db.close()  # Giải phóng kết nối