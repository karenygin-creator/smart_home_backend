from pydantic import BaseModel


class ScenarioCreate(BaseModel):
    name:str
    condition:str
    action:str
    house_id:int

class ScenarioUpdate(BaseModel):
    name:str
    condition:str
    action:str
    is_active:bool