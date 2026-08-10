from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import service
from schemas import ProductCreate


router = APIRouter(
    prefix="/api/v1/products",
    tags=["Product"]
)

@router.get("/")
def get_product(db:Session= Depends(get_db)):
    return service.get_product(db)

@router.post("/")
def post_product(input_product:ProductCreate,db:Session= Depends(get_db)):
    return service.post_product(input_product, db)

@router.put("/{id}")
def put_products(update_products:ProductCreate,id:int,db:Session= Depends(get_db)):
    return service.put_products(update_products, id, db)