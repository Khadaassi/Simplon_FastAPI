# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "supersecretkey"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = "sqlite:///./database.db"
    MODEL_PATH: str = "app/models/loan_model.pkl"  # Emplacement du modèle ML

    class Config:
        env_file = ".env"

settings = Settings()
