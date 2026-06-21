from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import verify_password, create_access_token
from database import get_db
from models.user import User


router = APIRouter(prefix="/auth", tags=["Auth"])
@router.post("/login")
def login(from_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==from_data.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Email or password incorrect")

    if not verify_password(from_data.password, user.password):
        raise HTTPException(status_code=404, detail="Email or password incorrect")
    token=create_access_token(data={"user_id":user.id})
    return {
        "access_token": token,
        "token_type": "bearer",
    }