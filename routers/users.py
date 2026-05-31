from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.user import UserCreate

router=APIRouter(prefix="/users", tags=["Users"])
@router.post("/")
def create_user(user: UserCreate,
                db:Session=Depends(get_db)):
    db_user=User(
        email=user.email,
        password=user.password,
        full_name=user.full_name,
    )
    db.add(db_user)
    db.commit()
    return {"message": "User created"}
@router.get("/")
def get_users(db:Session=Depends(get_db)):
    users = db.query(User).all()
    return users