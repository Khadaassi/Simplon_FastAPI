import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, create_engine, select
from fastapi.security import OAuth2PasswordBearer
from models.user import User , UserLogin
from core.security import verify_password, create_access_token
from core.config import settings


# OAuth2PasswordBearer pour récupérer le token dans les requêtes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

# Configuration de la base de données SQLite
engine = create_engine(settings.SQLITE_URL, connect_args={"check_same_thread": False})

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Fonction pour récupérer un utilisateur par email
def get_user(email: str, session: Session):
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user

# Route pour la connexion et la génération du JWT token
@app.post("/login")
def login(user_data: UserLogin, session: Session = Depends(lambda: Session(engine))):
    user = get_user(user_data.email, session)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

if __name__ == "__main__":
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)

