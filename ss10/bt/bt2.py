"""
| STT | Phương thức truy vấn hiện tại | Tình huống gây lỗi (Edge Case) | Phương thức thay thế an toàn hơn |
| 1 | ``.one()`` | Khi ``order_id`` không tồn tại (ví dụ: 999), SQLAlchemy ném ``NoResultFound``, hệ thống crash và trả về 500 Internal Server Error kèm Stack Trace | Dùng ``.first()`` để trả về ``None`` nếu không có dữ liệu, sau đó kiểm tra và ném ``HTTPException(status_code=404)`` để trả về lỗi bảo mật đồng nhất |
"""

from fastapi import FastAPI, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/ecommerce_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_name = Column(String(100))
    total_price = Column(Integer)


app = FastAPI()


@app.get("/orders/{order_id}")
def get_order_detail(order_id: int):
    db = SessionLocal()
    try:
        order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )
        return {"id": order.id, "customer": order.customer_name}
    finally:
        db.close()