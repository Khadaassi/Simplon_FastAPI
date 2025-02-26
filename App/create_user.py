# create_admin.py
from sqlmodel import Session, create_engine
from models.user import User
from core.security import hash_password
from core.config import settings

# Connexion à la base de données
engine = create_engine(settings.DATABASE_URL)

# Informations de l'administrateur
admin_email = "Raouf@bamk.com"
admin_password = "admin123"  # Utilisez un mot de passe plus sécurisé en production

# Création de l'administrateur
with Session(engine) as session:
    # Vérifier si l'administrateur existe déjà
    existing_admin = session.query(User).filter(User.email == admin_email).first()

    if existing_admin:
        print(f"L'administrateur {admin_email} existe déjà.")
    else:
        # Créer un nouvel administrateur
        new_admin = User(
            email=admin_email,
            hashed_password=hash_password(admin_password),
            is_admin=True,
            is_active=True  # Activer directement le compte
        )

        session.add(new_admin)
        session.commit()
        print(f"Administrateur {admin_email} créé avec succès!")