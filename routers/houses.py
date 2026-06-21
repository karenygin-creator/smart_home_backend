from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models.house import House
from models.user import User
from schemas.house import HouseUpdate, HouseCreate

router=APIRouter(prefix="/houses", tags=["Houses"])
@router.post("/")
def create_house(house: HouseCreate,
                 db:Session=Depends(get_db),
                 current_user:User=Depends(get_current_user)):
    user=db.query(User).filter(User.id==current_user.id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    new_house = House(
        name=house.name,
        address=house.address,
        user_id=current_user.id,
    )
    db.add(new_house)
    db.commit()
    db.refresh(new_house)
    return new_house
@router.get("/")
def get_houses(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    houses = db.query(House).filter(House.user_id == current_user.id).all()
    return houses
@router.get("/{house_id}")
def get_house(house_id: int, db:Session=Depends(get_db)
              ,current_user:User=Depends(get_current_user)):
    house = db.query(House).filter(House.id == house_id,House.user_id==current_user.id).first()
    if house is None:
        raise HTTPException(status_code=404, detail="House not found")
    return house

@router.put("/{house_id}")
def update_house(house_id: int, house_data: HouseUpdate,db:Session=Depends(get_db)
                 ,current_user:User=Depends(get_current_user)):
    house = db.query(House).filter(House.id == house_id,House.user_id==current_user.id).first()
    if house is None:
        raise HTTPException(status_code=404, detail="House not found")
    house.name = house_data.name
    house.address = house_data.address
    db.commit()
    db.refresh(house)
    return house
@router.delete("/{house_id}")
def delete_house(house_id: int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    house = db.query(House).filter(House.id == house_id,House.user_id==current_user.id).first()
    if house is None:
        raise HTTPException(status_code=404, detail="House not found")
    db.delete(house)
    db.commit()
    return {"message": "House deleted"}