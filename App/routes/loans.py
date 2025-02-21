# app/routes/loan.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.models.loans import LoanRequest
from app.database.database import get_session
import pickle
import pandas as pd
from app.schemas.loans import LoanApplication
from app.core.security import get_current_user
from datetime import datetime
from typing import Optional


router = APIRouter(prefix="/loans", tags=["Loans"])
# Charger le modèle une seule fois au démarrage
#MODEL_PATH = os.path.join(os.path.dirname(__file__), "loan_model.pkl")

with open("app/models/loan_model.pkl", "rb") as f:
    model = pickle.load(f)

FEATURES = ['State', 'NAICS', 'NewExist', 'RetainedJob', 
            'FranchiseCode', 'UrbanRural', 'GrAppv', 'Bank', 'Term']

@router.post("/predict")
def predict_loan_eligibility(application: LoanApplication, current_user: dict = Depends(get_current_user), db: Session = Depends(get_session)):
     # Convertir l'entrée en DataFrame pour le modèle
    input_data = pd.DataFrame([application.dict()])
    # Faire la prédiction
    prediction = model.predict(input_data)
    # Stocker la requête dans LoanRequest
    loan_request = LoanRequest(
        user_id=current_user["id"],  # ID de l'utilisateur connecté
        amount=application.GrAppv,   # Montant demandé
        status="approved" if prediction[0] == 1 else "denied",
        created_at=datetime.utcnow()
    )

    db.add(loan_request)
    db.commit()
    db.refresh(loan_request)

    # Retourner la prédiction (ex: 1 = Eligible, 0 = Non éligible)
    return {"eligible": bool(prediction[0]), "loan_request_id": loan_request.id}

@router.post("/request")
def request_loan(amount: float, user_id: int, session: Session = Depends(get_session)):
    loan_request = LoanRequest(user_id=user_id, amount=amount)
    session.add(loan_request)
    session.commit()
    return {"message": "Loan request submitted"}

@router.get("/history")
def get_loan_history(
    current_user: dict = Depends(get_current_user),  
    db: Session = Depends(get_session),
    status: Optional[str] = Query(None, description="Filtrer par statut (approved, denied, pending)")
):
    # Récupérer toutes les demandes de l'utilisateur
    query = select(LoanRequest).where(LoanRequest.user_id == current_user["id"])

    # Appliquer un filtre si un statut est donné
    if status:
        query = query.where(LoanRequest.status == status)

    loan_requests = db.exec(query).all()

    # Retourner l'historique des demandes
    return [
        {
            "id": request.id,
            "amount": request.amount,
            "status": request.status,
            "created_at": request.created_at
        }
        for request in loan_requests
    ]
@router.get("/history")
def loan_history():
    pass


@router.post("/request")
def predict_and_save_loan(
    application: LoanApplication, 
    db: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    # Faire la prédiction
    input_data = pd.DataFrame([application.dict()])
    prediction = model.predict(input_data)
    
    # Vérifier l'éligibilité
    is_eligible = bool(prediction[0])
    
    # Enregistrer la demande en DB
    loan_request = LoanRequest(
        user_id=current_user.id,  # récupérer l'utilisateur connecté
        amount=application.GrAppv,
        status="approved" if is_eligible else "rejected"
    )
    db.add(loan_request)
    db.commit()
    db.refresh(loan_request)
    
    return {
        "eligible": is_eligible,
        "status": loan_request.status,
        "loan_request_id": loan_request.id
    }
