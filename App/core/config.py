import os
from pydantic_settings import BaseSettings

dir_path = os.path.dirname(os.path.realpath(__file__))

class Settings(BaseSettings):
    APP_NAME: str = "Simplon_FastAPI"
    APP_VERSION: str = "0.0.1"
    SQLITE_URL: str = f"sqlite:///{dir_path}/database.db"

settings = Settings()