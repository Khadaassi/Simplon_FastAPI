# app/routes/loan.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from models.loans import LoanRequest
from database.database import get_session
import pickle
import pandas as pd
from schemas.loans import LoanApplication
from core.security import get_current_user
from datetime import datetime
from typing import Optional


router = APIRouter(prefix="/loans", tags=["Loans"])
# Charger le modèle une seule fois au démarrage
#MODEL_PATH = os.path.join(os.path.dirname(__file__), "loan_model.pkl")

with open("App/models/loan_model.pkl", "rb") as f:
    model = pickle.load(f)

FEATURES = ['State', 'NAICS', 'NewExist', 'RetainedJob', 
            'FranchiseCode', 'UrbanRural', 'GrAppv', 'Bank', 'Term']


@router.get("/history")
def get_loan_history(
    current_user: dict = Depends(get_current_user),  
    db: Session = Depends(get_session),
    status: Optional[str] = Query(None, description="Filtrer par statut (approved, denied, pending)")
):
    # Récupérer toutes les demandes de l'utilisateur
    query = select(LoanRequest).where(LoanRequest.user_id == current_user.id)

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

# app/routes/loan.py - Ajoutez cet endpoint
@router.get("/advisor")
def get_advisor_loans(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Récupère les prêts assignés à un conseiller"""
    # Vérifier si l'utilisateur est un conseiller
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé aux conseillers")

    # Récupérer tous les prêts
    loan_requests = db.exec(select(LoanRequest)).all()

    # Organiser les prêts par client
    client_loans = {}
    for loan in loan_requests:
        # Récupérer l'utilisateur qui a fait la demande
        user = db.exec(select(user).where(user.id == loan.user_id)).first()
        if user:
            if user.email not in client_loans:
                client_loans[user.email] = []
            client_loans[user.email].append({
                "id": loan.id,
                "amount": loan.amount,
                "status": loan.status,
                "created_at": loan.created_at.isoformat()
            })

    return client_loans