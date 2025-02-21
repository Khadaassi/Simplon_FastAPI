# app/models/user.py
from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str
    is_admin: bool = Field(default=False)
    is_active: bool = Field(default=False)
