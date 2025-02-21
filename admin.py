from sqlmodel import Session
from database.database import engine
from models.user import User
from core.security import hash_password

# Crée une session avec la DB
with Session(engine) as session:
    # Crée un utilisateur admin
    admin_user = User(
        email="admin1@example.com",
        hashed_password=hash_password("azerty123456"),
        is_active=True,
        is_admin=True  # Vérifie que ton modèle a ce champ
    )
    
    # Ajoute et sauvegarde l'utilisateur dans la DB
    session.add(admin_user)
    session.commit()
    session.refresh(admin_user)
    
    print("Utilisateur admin créé avec l'email :", admin_user.email)
