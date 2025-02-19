from sqlmodel import SQLModel, Field
from datetime import datetime

class LoanRequests(SQLModel, table=True):
    id : int = Field(default=None, primary_key=True)
    client_id : int
    amount : float
    date_of_request : datetime
    status : str

    def __str__(self):
        return f"{self.amount} - {self.client_id} - {self.status}"
