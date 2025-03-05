# app/core/security.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from App.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from App.core.config import settings
from App.database.database import get_session
from App.models.user import User

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Gestion des mots de passe
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# OAuth2 pour gérer l'authentification avec JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def get_admin_user(current_user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == current_user.email)).first()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
