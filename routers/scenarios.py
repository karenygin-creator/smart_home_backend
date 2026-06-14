from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import get_db
from models.house import House
from models.room import Room
from models.scenario import Scenario
from schemas.room import RoomCreate, RoomUpdate
from schemas.scenario import ScenarioCreate, ScenarioUpdate

router=APIRouter(prefix="/scenarios", tags=["Scenarios"])
@router.post("/")
def create_scenario(scenario: ScenarioCreate,
                 db:Session=Depends(get_db)):
    house=db.query(House).filter(House.id==scenario.house_id).first()
    if house is None:
        raise HTTPException(status_code=404, detail="House not found")
    new_scenario = Scenario(
        name=scenario.name,
        condition=scenario.condition,
        action=scenario.action,
        house_id=scenario.house_id
    )
    db.add(new_scenario)
    db.commit()
    db.refresh(new_scenario)
    return new_scenario

@router.get("/")
def get_scenarios(db:Session=Depends(get_db)):
    scenarios = db.query(Scenario).all()
    return scenarios
@router.get("/{scenario_id}")
def get_scenario(scenario_id: int, db:Session=Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario

@router.put("/{scenario_id}")
def update_scenario(scenario_id: int, scenario_data: ScenarioUpdate,db:Session=Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    scenario.name=scenario_data.name
    scenario.condition=scenario_data.condition
    scenario.action=scenario_data.action
    scenario.is_active=scenario_data.is_active
    db.commit()
    db.refresh(scenario)
    return scenario
@router.patch("/{scenario_id}/toggle")
def toggle_scenario(scenario_id: int, scenario_data: ScenarioUpdate,db:Session=Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    scenario.is_active=not scenario_data.is_active
    db.commit()
    db.refresh(scenario)
    return scenario
@router.delete("/{scenario_id}")
def delete_scenario(scenario_id: int,db:Session=Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    db.delete(scenario)
    db.commit()
    return {"message": "Scenario deleted"}