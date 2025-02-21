# app/main.py
from fastapi import FastAPI
import uvicorn
from app.database.database import init_db
from app.routes import auth, loan, admin

# Initialiser l'application FastAPI
app = FastAPI(
    title="Loan API",
    description="API de gestion des prêts avec prédiction",
    version="1.0"
)

# Initialisation de la base de données au démarrage
@app.on_event("startup")
def startup():
    init_db()

# Inclusion des routes
app.include_router(auth.router)
app.include_router(loan.router)
app.include_router(admin.router)

# Point d'entrée de test
@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API de prêt !"}

# Permet d'exécuter directement le script avec `python app/main.py`
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
