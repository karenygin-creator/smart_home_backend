from pydantic import BaseModel


class HouseCreate(BaseModel):
    name: str
    address: str

class HouseUpdate(BaseModel):
    name: str
    address: str
