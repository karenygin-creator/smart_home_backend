from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from auth import hash_password, get_current_user
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserUpdate

router=APIRouter(prefix="/users", tags=["Users"])
@router.post("/")
def create_user(user: UserCreate,
                db:Session=Depends(get_db)):
    db_user=User(
        email=user.email,
        password=hash_password(user.password),
        full_name=user.full_name,
    )
    db.add(db_user)
    db.commit()
    return {"message": "User created"}
@router.get("/")
def get_users(db:Session=Depends(get_db)):
    users = db.query(User).all()
    return users
@router.get("/me")
def get_users(current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    return current_user
@router.get("/{user_id}")
def get_user(user_id: int, db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

@router.put("/{user_id}")
def update_user(user_id: int,user_data:UserUpdate, db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.email = user_data.email
    user.password=user_data.password
    user.full_name=user_data.full_name
    db.commit()
    db.refresh(user)
    return user