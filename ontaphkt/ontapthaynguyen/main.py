from fastapi import FastAPI, Depends
from database import Base, engine
from models import DeviceModel
from sqlalchemy.orm import Session
from database import get_db
import TechRent_service 
from schemas import TechRentCreate

app= FastAPI(
    title="dịch vụ cho thuê thiết bị công nghệ làm việc từ xa"
)

Base.metadata.create_all(bind = engine)

@app.get("/")
def test_root():
    return "sever đang hoạt động"


# search&sort
@app.get("/devices")
def read_devices(
    category: str = None,
    status: str = None,
    sort_by: str = None,
    order: str = "asc",
    db: Session = Depends(get_db)
):
    return TechRent_service.get_devices(
        db=db,
        category=category,
        status=status,
        sort_by=sort_by,
        order=order
    )

@app.get("/devices/{device_id}")
def search(
    device_id:str,
    db:Session = Depends(get_db)):
    return TechRent_service.search(db, device_id)

@app.post("/devices")
def post_device(device: TechRentCreate, db:Session = Depends(get_db)):
    return TechRent_service.post_device(db, device)

@app.put("/devices/{device_id}")
def put_device(device_id:str, device:TechRentCreate,db:Session = Depends(get_db)):
    return TechRent_service.put_device(db,device,device_id)

@app.delete("/devices/{device_id}")
def delete(device_id:str,db:Session=Depends(get_db)):
    return TechRent_service.delete(db,device_id)