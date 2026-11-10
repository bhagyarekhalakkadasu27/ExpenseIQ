
from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, ConfigDict


class TransactionCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0)
    transaction_type: Literal["income", "expense"]
    category: str = Field(min_length=1, max_length=50)
    date: date
    description: Optional[str] = None


class TransactionUpdate(TransactionCreate):
    pass


class TransactionResponse(TransactionCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None
#code changes


class BudgetCreate(BaseModel):
    month: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")
    category: str = Field(min_length=1, max_length=50)
    amount: float = Field(gt=0)


class BudgetResponse(BudgetCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
