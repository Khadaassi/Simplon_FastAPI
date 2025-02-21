from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_admin: bool  # "admin" ou "user"

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool
    

    class Config:
        from_attributes = True

# Schéma pour la connexion (Login)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schéma pour la réponse après connexion (token JWT)
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"