
from sqlalchemy.orm import Session

from backend.app.models import Transaction
from backend.app.schemas import TransactionCreate, TransactionUpdate


# CREATE: Add a new transaction
def create_transaction(db: Session, transaction: TransactionCreate):
    db_transaction = Transaction(**transaction.model_dump())

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction


# READ: Get all transactions
def get_transactions(db: Session):
    return (
        db.query(Transaction)
        .order_by(Transaction.date.desc(), Transaction.id.desc())
        .all()
    )


# READ: Get one transaction by ID
def get_transaction(db: Session, transaction_id: int):
    return (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )


# UPDATE: Update an existing transaction
def update_transaction(
    db: Session,
    transaction_id: int,
    transaction: TransactionUpdate
):
    db_transaction = get_transaction(db, transaction_id)

    if db_transaction is None:
        return None

    updated_data = transaction.model_dump()

    for key, value in updated_data.items():
        setattr(db_transaction, key, value)

    db.commit()
    db.refresh(db_transaction)

    return db_transaction


# DELETE: Delete a transaction
def delete_transaction(db: Session, transaction_id: int):
    db_transaction = get_transaction(db, transaction_id)

    if db_transaction is None:
        return False

    db.delete(db_transaction)
    db.commit()

    return True
#code change


# ---------------- BUDGET OPERATIONS ----------------

from backend.app.models import Budget
from backend.app.schemas import BudgetCreate


# CREATE OR UPDATE BUDGET
def create_or_update_budget(db: Session, budget: BudgetCreate):

    existing_budget = (
        db.query(Budget)
        .filter(
            Budget.month == budget.month,
            Budget.category == budget.category
        )
        .first()
    )

    if existing_budget:
        existing_budget.amount = budget.amount
        db.commit()
        db.refresh(existing_budget)
        return existing_budget

    new_budget = Budget(**budget.model_dump())

    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)

    return new_budget


# GET ALL BUDGETS
def get_budgets(db: Session):
    return (
        db.query(Budget)
        .order_by(Budget.month.desc())
        .all()
    )


# DELETE BUDGET
def delete_budget(db: Session, budget_id: int):

    budget = (
        db.query(Budget)
        .filter(Budget.id == budget_id)
        .first()
    )

    if budget is None:
        return False

    db.delete(budget)
    db.commit()

    return True
