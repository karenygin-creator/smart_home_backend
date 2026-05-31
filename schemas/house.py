from pydantic import BaseModel


class HouseCreate(BaseModel):
    name: str
    address: str
    user_id: int
class HouseUpdate(BaseModel):
    name: str
    address: str
