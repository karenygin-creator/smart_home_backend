from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from auth import verify_password
from database import get_db
from models.user import User
from schemas.auth import LoginData

router = APIRouter(prefix="/auth", tags=["Auth"])
@router.post("/login")
def login(data:LoginData,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==data.email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Email or password incorrect")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=404, detail="Email or password incorrect")
    return {"message": "Login successful",
            "user_id": user.id,
            "email": user.email}