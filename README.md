# ExpenseIQ – Smart Expense Tracking & Financial Analytics Platform

## Project Overview

ExpenseIQ is a personal finance management application that helps users track income and expenses, analyze spending patterns, and manage monthly budgets through an interactive dashboard.

The application uses a Streamlit frontend, FastAPI backend, and Neon PostgreSQL database.

## Features

- Add, view, update, and delete transactions.
- Track income and expenses.
- View total income, expenses, and balance.
- Analyze expenses by category using charts.
- View monthly spending trends.
- Filter and export transaction data as CSV.
- Create and manage monthly category-wise budgets.
- Monitor budget usage and identify overspending.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Backend | FastAPI |
| Database | Neon PostgreSQL |
| ORM | SQLAlchemy |
| Data Analysis | Pandas |
| Visualizations | Plotly |
| API Communication | REST API |
| Environment Management | python-dotenv |

## Project Architecture

Streamlit Frontend → FastAPI REST API → SQLAlchemy → Neon PostgreSQL

## Project Structure

```text
ExpenseIQ/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── crud.py
│   └── __init__.py
├── frontend/
│   └── streamlit_app.py
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

## Installation and Setup

1. Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ExpenseIQ
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Neon PostgreSQL connection string:

```env
DATABASE_URL=your_neon_postgresql_connection_string
```

5. Start the FastAPI backend:

```bash
python -m uvicorn backend.app.main:app --reload
```

6. Open another terminal, activate the virtual environment, and start Streamlit:

```bash
python -m streamlit run frontend/streamlit_app.py
```

## API Documentation

Once the backend is running, visit:

`http://127.0.0.1:8000/docs`

FastAPI provides interactive API documentation through Swagger UI.

## Learning Outcomes

- Building REST APIs using FastAPI.
- Connecting Python applications to PostgreSQL.
- Performing database operations using SQLAlchemy.
- Developing interactive dashboards using Streamlit.
- Analyzing financial data using Pandas.
- Creating visualizations using Plotly.
- Managing application configuration and environment variables.

## Author

Developed as a hands-on Python, Data Analytics, and backend development project.