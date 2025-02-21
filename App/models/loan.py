# app/models/loan.py
from sqlmodel import SQLModel, Field
from typing import Optional

class LoanRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    amount: float
    status: str = "pending"

