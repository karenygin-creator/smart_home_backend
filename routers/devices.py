from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.device import Device
from models.house import House
from models.room import Room
from schemas.device import DeviceCreate, DeviceUpdate

router = APIRouter(prefix="/devices", tags=["Devices"])
@router.post("/")
def create_device(device:DeviceCreate,
                  db:Session=Depends(get_db)):
    house=db.query(House).filter(House.id==device.house_id).first()
    if house is None:
        raise HTTPException(status_code=404, detail="House not found")
    room = db.query(Room).filter(Room.id == device.room_id).first()
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    new_device = Device(
        name=device.name,
        type=device.type,
        house_id=device.house_id,
        room_id=device.room_id
    )
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device

@router.get("/")
def get_devices(db:Session=Depends(get_db)):
    devices = db.query(Device).all()
    return devices
@router.get("/{device_id}")
def get_device(device_id: int, db:Session=Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.put("/{device_id}")
def update_device(device_id: int, device_data: DeviceUpdate,db:Session=Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    device.name = device_data.name
    device.type = device_data.type
    device.status = device_data.status
    device.is_online = device_data.is_online
    db.commit()
    db.refresh(device)
    return device
@router.delete("/{device_id}")
def delete_device(device_id: int,db:Session=Depends(get_db)):
    device = db.query(Device).filter(Device.id ==device_id).first()
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(device)
    db.commit()
    return {"message": "Device deleted"}