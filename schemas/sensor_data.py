from pydantic import BaseModel


class SensorDataCreate(BaseModel):
    value: float
    unit: str
    device_id: int