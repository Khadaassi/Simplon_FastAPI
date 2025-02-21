# app/main.py
from fastapi import FastAPI
from app.database.database import create_db_and_tables
from app.routes import loans, admin, auth

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth.router)
app.include_router(loans.router)
app.include_router(admin.router)

# Lancer le serveur
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
