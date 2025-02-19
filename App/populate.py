from models.user import User
from sqlmodel import Session, create_engine, SQLModel
from core.database import engine

def create_user():
    with Session(engine) as session:
        user = User(id=1, email="test@test.com", password="azerty1234", role="admin")
        session.add(user)
        session.commit()
        session.refresh(user)

    return user

if __name__ == "__main__":
    new_user = create_user()
    print(f"Utilisateur créé : {new_user}")