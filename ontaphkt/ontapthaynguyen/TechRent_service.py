from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from models import DeviceModel 
from schemas import TechRentCreate
from fastapi import FastAPI, HTTPException, status

# search & sort
def get_devices(
    db: Session,
    category: str = None,
    status: str = None,
    sort_by: str = None,
    order: str = "asc"
):
    query = db.query(DeviceModel)
    if category:
        query = query.filter(
            DeviceModel.category.like(f"%{category}%")
        )
    if status:
        query = query.filter(
            DeviceModel.status == status
        )
    if sort_by == "rental_rate":
        if order == "desc":
            query = query.order_by(
                desc(DeviceModel.rental_rate)
            )
        else:
            query = query.order_by(
                asc(DeviceModel.rental_rate)
            )
    elif sort_by == "release_year":

        if order == "desc":
            query = query.order_by(
                desc(DeviceModel.release_year)
            )

        else:
            query = query.order_by(
                asc(DeviceModel.release_year)
            )
    else:
        query = query.order_by(
            asc(DeviceModel.id)
        )
    devices = query.all()

    return devices

def search(db: Session , device_id:str):
    return db.query(DeviceModel).filter(DeviceModel.id == device_id).first()

def post_device(db:Session, device:TechRentCreate):
    new_device = DeviceModel(
        id= device.id,
        category = device.category,
        model = device.model,
        rental_rate  = device.rental_rate,
        release_year = device.release_year,
        status = device.status
    )
    exist = db.query(DeviceModel).filter(
        DeviceModel.id == device.id
    ).first()

    if exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="id trùng"
        )
    db.add(new_device)
    db.commit()
    db.refresh(new_device)

    return new_device

def put_device(db:Session, input_device:TechRentCreate, device_id:str):
    find_id = db.query(DeviceModel).filter(DeviceModel.id == device_id).first()
    if not find_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="không tìm thấy id")
    
    find_id.category = input_device.category
    find_id.model = input_device.model
    find_id.rental_rate = input_device.rental_rate
    find_id.release_year = input_device.release_year
    find_id.status = input_device.status
    
    db.commit()
    db.refresh(find_id)

    return find_id


def delete(db:Session, device_id:str):
    find_id = db.query(DeviceModel).filter(DeviceModel.id == device_id).first()
    if not find_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="không tìm thấy id")
    db.delete(find_id)
    db.commit()
    return find_id