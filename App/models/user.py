from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id : int = Field(primary_key=True)
    email : str
    password : str
    is_active : bool = False
    role : str

    def __str__(self):
        return f"{self.email} - {self.role}"

class UserLogin(SQLModel):
    email: str
    password: str