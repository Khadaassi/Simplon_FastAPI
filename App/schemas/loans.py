from pydantic import BaseModel

class LoanApplication(BaseModel):
    State: str
    NAICS: int
    NewExist: int
    RetainedJob: int
    FranchiseCode: int
    UrbanRural: int
    GrAppv: float
    Bank: str
    Term: int