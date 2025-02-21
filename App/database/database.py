# app/database/database.py
from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings

# Création de l'engine de la base de données
engine = create_engine(settings.DATABASE_URL, echo=True)

# Fonction pour initialiser la base de données
def init_db():
    SQLModel.metadata.create_all(engine)

# Dépendance pour obtenir une session de base de données
def get_db():
    with Session(engine) as session:
        yield session
