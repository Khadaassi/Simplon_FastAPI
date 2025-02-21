# app/routes/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.user import User
from app.core.security import hash_password
from app.core.security import get_current_user
from app.database.database import get_session
from app.schemas.users import UserCreate
from app.core.security import get_admin_user

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/admin/users", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_session), admin: User = Depends(get_admin_user)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        is_admin=user.is_admin
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Utilisateur créé avec succès"}

@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"email": current_user["sub"], "role": current_user.get("role")}
