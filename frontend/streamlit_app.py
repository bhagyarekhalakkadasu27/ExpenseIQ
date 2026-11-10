
import os
import re
import requests
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

# ---------------- CONFIGURATION ----------------

load_dotenv()

API_URL = os.getenv("API_URL", "https://expenseiq-1-3ynz.onrender.com")
st.set_page_config(
    page_title="ExpenseIQ | Smart Finance",
    page_icon="💰",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 2rem;
    }

    [data-testid="stMetric"] {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e6eaf0;
    }

    h1, h2, h3 {
        color: #172554;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- TRANSACTION API FUNCTIONS ----------------

def get_transactions():
    try:
        response = requests.get(
            f"{API_URL}/transactions",
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        st.error(f"Unable to connect to ExpenseIQ API: {error}")
        return None


def get_summary():
    try:
        response = requests.get(
            f"{API_URL}/summary",
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        st.error(f"Unable to load financial summary: {error}")
        return None


def add_transaction(data):
    try:
        response = requests.post(
            f"{API_URL}/transactions",
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return True

    except requests.RequestException as error:
        st.error(f"Unable to add transaction: {error}")
        return False


def update_transaction(transaction_id, data):
    try:
        response = requests.put(
            f"{API_URL}/transactions/{transaction_id}",
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return True

    except requests.RequestException as error:
        st.error(f"Unable to update transaction: {error}")
        return False


def delete_transaction(transaction_id):
    try:
        response = requests.delete(
            f"{API_URL}/transactions/{transaction_id}",
            timeout=10
        )
        response.raise_for_status()
        return True

    except requests.RequestException as error:
        st.error(f"Unable to delete transaction: {error}")
        return False


# ---------------- BUDGET API FUNCTIONS ----------------

def get_budgets():
    try:
        response = requests.get(
            f"{API_URL}/budgets",
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        st.error(f"Unable to load budgets: {error}")
        return None


def save_budget(data):
    try:
        response = requests.post(
            f"{API_URL}/budgets",
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return True

    except requests.RequestException as error:
        st.error(f"Unable to save budget: {error}")
        return False


def delete_budget(budget_id):
    try:
        response = requests.delete(
            f"{API_URL}/budgets/{budget_id}",
            timeout=10
        )
        response.raise_for_status()
        return True

    except requests.RequestException as error:
        st.error(f"Unable to delete budget: {error}")
        return False


# ---------------- SIDEBAR NAVIGATION ----------------

st.sidebar.title("💰 ExpenseIQ")

st.sidebar.caption("Smart Expense Tracking")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Transaction",
        "Manage Transactions",
        "Budget Management"
    ]
)

st.sidebar.divider()

st.sidebar.caption("Track smarter. Save better.")


# ---------------- HEADER ----------------

st.title("💰 ExpenseIQ")

st.write("Your personal financial analytics dashboard.")

st.divider()


# ---------------- FETCH DATA ----------------

transactions = get_transactions()

if transactions is None:
    st.stop()

summary = get_summary()

if summary is None:
    st.stop()

df = pd.DataFrame(transactions)

if not df.empty:
    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = pd.to_numeric(df["amount"])


# =====================================================
# DASHBOARD PAGE
# =====================================================

if page == "Dashboard":

    st.subheader("Financial Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Income",
        f"₹{summary['total_income']:,.2f}"
    )

    col2.metric(
        "Total Expenses",
        f"₹{summary['total_expenses']:,.2f}"
    )

    col3.metric(
        "Available Balance",
        f"₹{summary['balance']:,.2f}"
    )

    col4.metric(
        "Transactions",
        summary["total_transactions"]
    )

    st.divider()

    if df.empty:

        st.info(
            "No transactions available. Add your first transaction!"
        )

    else:

        # ---------------- TRANSACTION FILTERS ----------------

        st.subheader("Transaction Filters")

        col1, col2 = st.columns(2)

        with col1:
            transaction_type = st.selectbox(
                "Transaction Type",
                ["All", "income", "expense"]
            )

        with col2:
            categories = ["All"] + sorted(
                df["category"].dropna().unique().tolist()
            )

            selected_category = st.selectbox(
                "Category",
                categories
            )

        filtered_df = df.copy()

        if transaction_type != "All":
            filtered_df = filtered_df[
                filtered_df["transaction_type"] == transaction_type
            ]

        if selected_category != "All":
            filtered_df = filtered_df[
                filtered_df["category"] == selected_category
            ]

        st.divider()

        # ---------------- FINANCIAL CHARTS ----------------

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Income vs Expenses")

            chart_data = pd.DataFrame({
                "Type": ["Income", "Expenses"],
                "Amount": [
                    summary["total_income"],
                    summary["total_expenses"]
                ]
            })

            fig = px.pie(
                chart_data,
                names="Type",
                values="Amount",
                hole=0.5,
                title="Financial Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            st.subheader("Category-wise Expenses")

            expense_df = filtered_df[
                filtered_df["transaction_type"] == "expense"
            ]

            if not expense_df.empty:

                category_data = (
                    expense_df.groupby("category")["amount"]
                    .sum()
                    .reset_index()
                )

                fig = px.bar(
                    category_data,
                    x="category",
                    y="amount",
                    title="Expenses by Category",
                    labels={
                        "category": "Category",
                        "amount": "Amount (₹)"
                    }
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.info("No expense data for this selection.")

        st.divider()

        # ---------------- MONTHLY FINANCIAL ANALYTICS ----------------

        st.subheader("📈 Monthly Financial Trends")

        monthly_df = df.copy()

        monthly_df["month"] = (
            monthly_df["date"].dt.to_period("M").astype(str)
        )

        monthly_summary = (
            monthly_df.groupby(
                ["month", "transaction_type"]
            )["amount"]
            .sum()
            .reset_index()
        )

        monthly_pivot = monthly_summary.pivot(
            index="month",
            columns="transaction_type",
            values="amount"
        ).fillna(0).reset_index()

        if "income" not in monthly_pivot.columns:
            monthly_pivot["income"] = 0

        if "expense" not in monthly_pivot.columns:
            monthly_pivot["expense"] = 0

        monthly_pivot = monthly_pivot.sort_values("month")

        fig = px.line(
            monthly_pivot,
            x="month",
            y=["income", "expense"],
            markers=True,
            title="Monthly Income vs Expenses",
            labels={
                "month": "Month",
                "value": "Amount (₹)",
                "variable": "Transaction Type"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        # ---------------- RECENT TRANSACTIONS ----------------

        st.subheader("Recent Transactions")

        display_df = filtered_df.sort_values(
            "date",
            ascending=False
        )

        st.dataframe(
            display_df[
                [
                    "id",
                    "title",
                    "amount",
                    "transaction_type",
                    "category",
                    "date"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        # ---------------- CSV EXPORT ----------------

        csv = display_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "📥 Download Transactions CSV",
            data=csv,
            file_name="expenseiq_transactions.csv",
            mime="text/csv"
        )


# =====================================================
# ADD TRANSACTION PAGE
# =====================================================

elif page == "Add Transaction":

    st.subheader("Add a New Transaction")

    with st.form("transaction_form"):

        title = st.text_input(
            "Transaction Title",
            placeholder="Example: Grocery Shopping"
        )

        col1, col2 = st.columns(2)

        with col1:

            amount = st.number_input(
                "Amount (₹)",
                min_value=0.01,
                step=100.0
            )

            transaction_type = st.selectbox(
                "Transaction Type",
                ["expense", "income"]
            )

        with col2:

            category = st.selectbox(
                "Category",
                [
                    "Food",
                    "Shopping",
                    "Travel",
                    "Bills",
                    "Salary",
                    "Business",
                    "Healthcare",
                    "Education",
                    "Entertainment",
                    "Other"
                ]
            )

            transaction_date = st.date_input(
                "Transaction Date"
            )

        description = st.text_area(
            "Description",
            placeholder="Add additional details..."
        )

        submitted = st.form_submit_button(
            "Add Transaction",
            use_container_width=True
        )

        if submitted:

            if not title.strip():

                st.warning("Please enter a transaction title.")

            else:

                data = {
                    "title": title.strip(),
                    "amount": amount,
                    "transaction_type": transaction_type,
                    "category": category,
                    "date": transaction_date.isoformat(),
                    "description": description
                }

                if add_transaction(data):

                    st.success("Transaction added successfully!")

                    st.rerun()


# =====================================================
# MANAGE TRANSACTIONS PAGE
# =====================================================

elif page == "Manage Transactions":

    st.subheader("Manage Your Transactions")

    if df.empty:

        st.info("No transactions available.")

    else:

        st.write("### Edit or Delete a Transaction")

        transaction_options = {
            f"{row['id']} - {row['title']} (₹{row['amount']:,.2f})":
            row["id"]
            for _, row in df.iterrows()
        }

        selected_label = st.selectbox(
            "Select Transaction",
            list(transaction_options.keys())
        )

        selected_id = transaction_options[selected_label]

        selected_transaction = next(
            item for item in transactions
            if item["id"] == selected_id
        )

        st.divider()

        # ---------------- EDIT TRANSACTION ----------------

        with st.form("edit_transaction_form"):

            edit_title = st.text_input(
                "Title",
                value=selected_transaction["title"]
            )

            col1, col2 = st.columns(2)

            with col1:

                edit_amount = st.number_input(
                    "Amount (₹)",
                    min_value=0.01,
                    value=float(selected_transaction["amount"]),
                    step=100.0
                )

                edit_type = st.selectbox(
                    "Transaction Type",
                    ["income", "expense"],
                    index=(
                        0 if selected_transaction["transaction_type"]
                        == "income" else 1
                    )
                )

            with col2:

                category_options = [
                    "Food",
                    "Shopping",
                    "Travel",
                    "Bills",
                    "Salary",
                    "Business",
                    "Healthcare",
                    "Education",
                    "Entertainment",
                    "Other"
                ]

                old_category = selected_transaction["category"]

                if old_category not in category_options:
                    category_options.append(old_category)

                edit_category = st.selectbox(
                    "Category",
                    category_options,
                    index=category_options.index(old_category)
                )

                edit_date = st.date_input(
                    "Date",
                    value=pd.to_datetime(
                        selected_transaction["date"]
                    ).date()
                )

            edit_description = st.text_area(
                "Description",
                value=selected_transaction["description"] or ""
            )

            update_clicked = st.form_submit_button(
                "Update Transaction",
                use_container_width=True
            )

            if update_clicked:

                if not edit_title.strip():

                    st.warning("Please enter a title.")

                else:

                    updated_data = {
                        "title": edit_title.strip(),
                        "amount": edit_amount,
                        "transaction_type": edit_type,
                        "category": edit_category,
                        "date": edit_date.isoformat(),
                        "description": edit_description
                    }

                    if update_transaction(
                        selected_id,
                        updated_data
                    ):

                        st.success("Transaction updated successfully!")

                        st.rerun()

        st.divider()

        # ---------------- DELETE TRANSACTION ----------------

        st.write("### Delete Transaction")

        st.warning(
            "Deleting a transaction is permanent."
        )

        confirm_delete = st.checkbox(
            "I confirm that I want to delete this transaction."
        )

        if st.button(
            "🗑️ Delete Selected Transaction",
            type="primary",
            disabled=not confirm_delete
        ):

            if delete_transaction(selected_id):

                st.success("Transaction deleted successfully!")

                st.rerun()


# =====================================================
# BUDGET MANAGEMENT PAGE
# =====================================================

elif page == "Budget Management":

    st.subheader("🎯 Monthly Budget Management")

    current_month = pd.Timestamp.today().strftime("%Y-%m")

    # ---------------- CREATE BUDGET ----------------

    st.write("### Set Your Monthly Budget")

    with st.form("budget_form"):

        budget_month = st.text_input(
            "Budget Month (YYYY-MM)",
            value=current_month
        )

        budget_category = st.selectbox(
            "Category",
            [
                "Food",
                "Shopping",
                "Travel",
                "Bills",
                "Healthcare",
                "Education",
                "Entertainment",
                "Other"
            ]
        )

        budget_amount = st.number_input(
            "Monthly Budget Amount (₹)",
            min_value=1.0,
            value=5000.0,
            step=500.0
        )

        save_clicked = st.form_submit_button(
            "Save Budget",
            use_container_width=True
        )

        if save_clicked:

            if not re.fullmatch(
                r"\d{4}-(0[1-9]|1[0-2])",
                budget_month
            ):

                st.error(
                    "Enter a valid month in YYYY-MM format."
                )

            else:

                budget_data = {
                    "month": budget_month,
                    "category": budget_category,
                    "amount": budget_amount
                }

                if save_budget(budget_data):

                    st.success("Budget saved successfully!")

                    st.rerun()

    st.divider()

    # ---------------- DISPLAY BUDGETS ----------------

    st.subheader("Your Budget Overview")

    budgets = get_budgets()

    if budgets is None:

        st.warning("Could not retrieve budgets.")

    elif not budgets:

        st.info("No budgets created yet.")

    else:

        selected_month = st.selectbox(
            "Select Month",
            sorted(
                {budget["month"] for budget in budgets},
                reverse=True
            )
        )

        monthly_budgets = [
            budget for budget in budgets
            if budget["month"] == selected_month
        ]

        for budget in monthly_budgets:

            category = budget["category"]

            budget_limit = float(budget["amount"])

            monthly_expenses = sum(
                float(transaction["amount"])
                for transaction in transactions
                if transaction["transaction_type"] == "expense"
                and transaction["category"] == category
                and transaction["date"][:7] == selected_month
            )

            remaining = budget_limit - monthly_expenses

            progress = min(
                monthly_expenses / budget_limit,
                1.0
            )

            st.write(f"### {category}")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Budget",
                f"₹{budget_limit:,.2f}"
            )

            col2.metric(
                "Spent",
                f"₹{monthly_expenses:,.2f}"
            )

            col3.metric(
                "Remaining",
                f"₹{remaining:,.2f}"
            )

            st.progress(progress)

            if remaining < 0:

                st.error(
                    "You have exceeded this category's budget!"
                )

            elif progress >= 0.8:

                st.warning(
                    "You have used at least 80% of your budget."
                )

            else:

                st.success(
                    "You are within your budget."
                )

            # ---------------- DELETE BUDGET ----------------

            if st.button(
                f"Delete {category} Budget",
                key=f"delete_budget_{budget['id']}"
            ):

                if delete_budget(budget["id"]):

                    st.success("Budget deleted successfully!")

                    st.rerun()

            st.divider()
