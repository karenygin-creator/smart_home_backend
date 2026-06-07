from pydantic import BaseModel


class RoomCreate(BaseModel):
    name:str
    house_id:int


class RoomUpdate(BaseModel):
    name:str