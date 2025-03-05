# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from App.models.user import User
from App.schemas.users import UserLogin, TokenResponse, UserActivation
from App.core.security import verify_password, create_access_token, hash_password
from App.core.config import settings
from App.database.database import get_session
from datetime import timedelta


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == user_data.email)).first()

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not user.is_active:
        return JSONResponse(
            status_code=403,
            content={
                "detail": "Your account is not activated. Please reset your password to activate it.",
                "redirect": "/auth/activation"
            }
        )

    print(f"DEBUG: User found: {user}")
    print(f"DEBUG: Hashed password in DB: {user.hashed_password}")

    return TokenResponse(access_token=create_access_token({"sub": user.email}), token_type="bearer")


@router.post("/activation")
def activate_account(user_data: UserActivation, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == user_data.email)).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    user.hashed_password = hash_password(user_data.new_password)
    user.is_active = True
    session.add(user)
    session.commit()
    return {"message": "Account activated"}
