import os
from dotenv import load_dotenv
from datetime import timezone, timedelta, datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
from models.user import User

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)
def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def create_access_token(data:dict):
    to_encode = data.copy()
    expire=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token
def get_current_user(token: str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id=payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Not found")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token invalid")
    user=db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User Not found")
    return user