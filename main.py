from fastapi import FastAPI

from database import Base, engine
from routers.auth_router import router as auth_router
from routers.devices import router as devices_router
from routers.houses import router as houses_router
from routers.rooms import router as rooms_router
from routers.scenarios import router as scenarios_router
from routers.sensor_data import router as sensor_data_router
from routers.users import router as users_router

app=FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(users_router)
app.include_router(houses_router)
app.include_router(rooms_router)
app.include_router(devices_router)
app.include_router(sensor_data_router)
app.include_router(scenarios_router)
app.include_router(auth_router)
@app.get("/")
def home():
    return {"message": "API works"}