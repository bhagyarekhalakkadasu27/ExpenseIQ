
from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.sql import func

from backend.app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False)

    amount = Column(Float, nullable=False)

    transaction_type = Column(String(20), nullable=False)
    # income or expense

    category = Column(String(50), nullable=False)

    date = Column(Date, nullable=False)

    description = Column(String(255), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
#pasting new code here


from sqlalchemy import UniqueConstraint


class Budget(Base):
    __tablename__ = "budgets"

    __table_args__ = (
        UniqueConstraint(
            "month",
            "category",
            name="uq_budget_month_category"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    month = Column(String(7), nullable=False)
    # Example: 2026-11

    category = Column(String(50), nullable=False)

    amount = Column(Float, nullable=False)
    # Monthly budget limit
