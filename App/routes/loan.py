# app/routes/loan.py
from fastapi import APIRouter, Depends
import pandas as pd
from sqlmodel import Session
from app.models.loan import LoanRequest
from app.core.ml_model import model
from app.core.security import get_current_user
from app.database.database import get_db
from app.schemas.loans import LoanApplication


router = APIRouter(prefix="/loans", tags=["loans"])

@router.get("/history")
def loan_history():
    pass


@router.post("/request")
def predict_and_save_loan(
    application: LoanApplication, 
    db: Session = Depends(get_db),
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
