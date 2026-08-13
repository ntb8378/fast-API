from sqlalchemy.orm import Session
from database import Base
from models import Warehouse, Package, Waybill
import schemas

def create_warehouse(db: Session, warehouse : schemas.WarehouseCreate):
    