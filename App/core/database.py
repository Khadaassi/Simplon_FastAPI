from sqlmodel import SQLModel, create_engine, Session
from core.config import settings

# # Database setup
engine = create_engine(settings.SQLITE_URL, connect_args={"check_same_thread":False})
SQLModel.metadata.create_all(engine)

# Dependency
def get_db():
    with Session(engine) as session:
        yield session
