from sqlalchemy.orm import Session
from models import ProductModel, CategoryModel
from schemas import ProductCreate, ProductUpdate
from fastapi import HTTPException

def get_product(db: Session):
    return db.query(ProductModel).all()

def post_product(input_product:ProductCreate,db:Session):
    new_product = ProductModel(
        product_code = input_product.product_code,
        name = input_product.name,
        price = input_product.price,
        stock_quantity = input_product.stock_quantity,
        category_id = input_product.category_id
    )

    find_product_code = db.query(ProductModel).filter(ProductModel.product_code == input_product.product_code).first()
    if find_product_code:
        raise HTTPException(
            status_code=400,
            detail="product_code không được trùng"
        )
    find_category_id = db.query(CategoryModel).filter(CategoryModel.id == input_product.category_id).first()
    if not find_category_id:
            raise HTTPException(
                status_code=404,
                detail="không có category_id này"
            )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

def put_products(update_products:ProductUpdate,id:int,db:Session):
    find_id = db.query(ProductModel).filter(ProductModel.id == id).first()
    if find_id:
        data = update_products.model_dump()

        for key, value in data.items():
            setattr(find_id, key, value)

        db.commit()
        db.refresh(find_id)

    return find_id




