from sqlmodel import SQLModel, Field
from typing import Optional


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
