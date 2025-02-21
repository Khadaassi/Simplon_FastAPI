# app/routes/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.user import User
from core.security import hash_password
from core.security import get_current_user
from database.database import get_session
from schemas.users import UserCreate
from core.security import get_admin_user

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/users", status_code=201)
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

@router.get("/users", status_code=200)
def get_users(session: Session = Depends(get_session), admin: User = Depends(get_admin_user)):
    users = session.exec(select(User)).all()
    return users
