from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.device import Device
from models.house import House
from models.room import Room
from models.sensor_data import SensorData

from schemas.sensor_data import SensorDataCreate

router = APIRouter(prefix="/sensor-data", tags=["Sensor Data"])
@router.post("/")
def create_sensor_data(data:SensorDataCreate,
                  db:Session=Depends(get_db)):
    device=db.query(Device).filter(Device.id==data.device_id).first()
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    new_data = SensorData(
        value=data.value,
        unit=data.unit,
        device_id=data.device_id
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

@router.get("/")
def get_all_sensor_data(db:Session=Depends(get_db)):
    data = db.query(SensorData).all()
    return data

@router.get("/device/{device_id}")
def get_sensor_data_by_device(device_id: int, db:Session=Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    data = db.query(SensorData).filter(SensorData.device_id == device_id).all()
    return data

@router.delete("/{data_id}")
def delete_sensor_data(data_id: int,db:Session=Depends(get_db)):
    data = db.query(SensorData).filter(SensorData.id ==data_id).first()
    if data is None:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(data)
    db.commit()
    return {"message": "Sensor Data deleted"}

