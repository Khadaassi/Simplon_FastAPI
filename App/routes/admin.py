# app/routes/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.user import User, UserRole
from app.core.security import hash_password
from app.core.security import get_current_user
from app.database.database import get_db

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users")
def get_users(db: Session = Depends(get_db), admin=Depends(get_current_user)):
    if admin.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.exec(select(User)).all()

@router.get("/users")
def list_users():
    pass

@router.post("/users")
def create_user(email: str, password: str, role: UserRole, db: Session = Depends(get_db), admin=Depends(get_current_user)):
    if admin.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    user = User(email=email, hashed_password=hash_password(password), role=role, is_active=False)
    db.add(user)
    db.commit()
    return {"message": "User created successfully"}
