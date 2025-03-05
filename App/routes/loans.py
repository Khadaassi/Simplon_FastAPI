# app/routes/loan.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from App.models.loans import LoanRequest
from App.database.database import get_session
import pickle
import pandas as pd
from App.schemas.loans import LoanApplication
from App.core.security import get_current_user
from datetime import datetime
from typing import Optional
import shap
import matplotlib.pyplot as plt
from io import BytesIO
import base64


router = APIRouter(prefix="/loans", tags=["Loans"])
# Charger le modèle une seule fois au démarrage
#MODEL_PATH = os.path.join(os.path.dirname(__file__), "loan_model.pkl")

with open("App/models/loan_model.pkl", "rb") as f:
    model = pickle.load(f)

FEATURES = ['State', 'NAICS', 'NewExist', 'RetainedJob', 
            'FranchiseCode', 'UrbanRural', 'GrAppv', 'Bank', 'Term']
# Extraire le modèle CatBoost de la pipeline
catboost_model = model.named_steps["model"]  # Récupérer le modèle entraîné

# Créer l'explainer SHAP
explainer = shap.Explainer(catboost_model)


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

def generate_shap_plot(model, input_data):
    explainer = shap.Explainer(model)
    shap_values = explainer(input_data)

    plt.figure(figsize=(8, 4))
    #shap.summary_plot(shap_values, input_data, plot_type="bar", show=False)
    shap.plots.waterfall(shap_values[0])

    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close()

    # Encoder l'image en Base64
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

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
    # Générer l'explication SHAP
    shap_plot = generate_shap_plot(catboost_model, input_data)
    
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
        "loan_request_id": loan_request.id,
        "shap_plot": shap_plot
    }
