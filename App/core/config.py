from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    DATABASE_URL: str
    MODEL_PATH: str

    class Config:
        env_file = ".env"  # Charge le fichier .env

settings = Settings()
