from sqlmodel import SQLModel, Field


class LoanRequests(SQLModel, table=True):
    id : int = Field(default=None, primary_key=True)
    amount : float
    client_id : int
    status : str

    def __str__(self):
        return f"{self.amount} - {self.client_id} - {self.status}"
