# app/models/loan.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class LoanRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    amount: float
    status: str = Field(default="pending")
    created_at: datetime = Field(default_factory=datetime.utcnow)
