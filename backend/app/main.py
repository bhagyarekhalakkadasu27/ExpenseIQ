
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import Base, engine, get_db
from backend.app import crud, schemas, models

# Create database tables automatically
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="ExpenseIQ API",
    description="Smart Expense Tracking and Financial Analytics Platform",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to ExpenseIQ API",
        "status": "Running successfully"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# CREATE TRANSACTION
@app.post("/transactions", response_model=schemas.TransactionResponse)
def add_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db)
):
    return crud.create_transaction(db, transaction)


# GET ALL TRANSACTIONS
@app.get("/transactions", response_model=list[schemas.TransactionResponse])
def get_all_transactions(db: Session = Depends(get_db)):
    return crud.get_transactions(db)


# GET TRANSACTION BY ID
@app.get("/transactions/{transaction_id}", response_model=schemas.TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = crud.get_transaction(db, transaction_id)

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction


# UPDATE TRANSACTION
@app.put("/transactions/{transaction_id}", response_model=schemas.TransactionResponse)
def edit_transaction(
    transaction_id: int,
    transaction: schemas.TransactionUpdate,
    db: Session = Depends(get_db)
):
    updated_transaction = crud.update_transaction(
        db, transaction_id, transaction
    )

    if updated_transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return updated_transaction


# DELETE TRANSACTION
@app.delete("/transactions/{transaction_id}")
def remove_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.delete_transaction(db, transaction_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return {"message": "Transaction deleted successfully"}


# FINANCIAL SUMMARY
@app.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    transactions = crud.get_transactions(db)

    total_income = sum(
        t.amount for t in transactions
        if t.transaction_type == "income"
    )

    total_expenses = sum(
        t.amount for t in transactions
        if t.transaction_type == "expense"
    )

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "balance": round(total_income - total_expenses, 2),
        "total_transactions": len(transactions)
    }
#code change


# ---------------- BUDGET API ENDPOINTS ----------------

# CREATE OR UPDATE BUDGET
@app.post("/budgets", response_model=schemas.BudgetResponse)
def add_or_update_budget(
    budget: schemas.BudgetCreate,
    db: Session = Depends(get_db)
):
    return crud.create_or_update_budget(db, budget)


# GET ALL BUDGETS
@app.get("/budgets", response_model=list[schemas.BudgetResponse])
def get_all_budgets(db: Session = Depends(get_db)):
    return crud.get_budgets(db)


# DELETE BUDGET
@app.delete("/budgets/{budget_id}")
def remove_budget(
    budget_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.delete_budget(db, budget_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Budget not found"
        )

    return {"message": "Budget deleted successfully"}
