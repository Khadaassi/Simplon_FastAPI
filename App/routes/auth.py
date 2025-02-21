# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.user import User
from app.schemas.users import UserLogin, TokenResponse
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.database.database import get_session
from datetime import timedelta


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == user_data.email)).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    print(f"DEBUG: User found: {user}")
    print(f"DEBUG: Hashed password in DB: {user.hashed_password}")
    return TokenResponse(access_token=create_access_token({"sub": user.email}), token_type="bearer")
