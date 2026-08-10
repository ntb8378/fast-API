from database import Base
from sqlalchemy import Column, Integer,Float, String, ForeignKey, Enum as sqlEnum, DateTime
from sqlalchemy.orm import relationship
from enum import Enum

class OderStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class CategoryModel(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True) 
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255),nullable=True)

    products = relationship("ProductModel" , back_populates="categories")

class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_code = Column(String(10), nullable=False, unique=True)
    name = Column(String(100), nullable= False) 
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default= 0)
    category_id = Column(Integer, ForeignKey("categories.id"))

    categories = relationship("CategoryModel", back_populates= "products")

    order_items= relationship("OrderItemModel", back_populates="products")

class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True , autoincrement= True)
    order_code = Column(String(20), nullable= False, unique=True)
    customer_name = Column(String(100), nullable= False)
    total_amount = Column(Float, default= 0.0)
    status = Column(sqlEnum(OderStatus))
    created_at = Column(DateTime)

    order_items = relationship("OrderItemModel",back_populates="orders",cascade="all, delete-orphan")


class OrderItemModel(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Integer, nullable= False)

    products = relationship("ProductModel", back_populates="order_items")
    orders = relationship("OrderModel", back_populates="order_items")