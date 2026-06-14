from pydantic import BaseModel

class DeviceCreate(BaseModel):
    name:str
    type:str
    house_id:int
    room_id:int
class DeviceUpdate(BaseModel):
    name:str
    type:str
    status:str
    is_online:bool

class DeviceStatusUpdate(BaseModel):
    status:str