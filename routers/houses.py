from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import get_db
from models.house import House
from models.user import User
from schemas.house import HouseUpdate, HouseCreate

router=APIRouter(prefix="/houses", tags=["Houses"])
@router.post("/")
def create_house(house: HouseCreate,
                 db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==house.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    new_house = House(
        name=house.name,
        address=house.address,
        user_id=house.user_id,
    )
    db.add(new_house)
    db.commit()
    db.refresh(new_house)
    return new_house