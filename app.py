
import streamlit as st
import sqlite3
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# Database connection
def get_connection():
    return sqlite3.connect("expenses.db")

# Page title
st.title("💰 Personal Expense Tracker")
st.write("Manage and track your daily expenses easily.")

# Fetch expenses
def get_expenses():
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM expenses ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

# Dashboard
df = get_expenses()

total = df["amount"].sum() if not df.empty else 0
count = len(df)
average = total / count if count > 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric("Total Expenses", f"₹{total:,.2f}")
col2.metric("Total Transactions", count)
col3.metric("Average Expense", f"₹{average:,.2f}")

st.divider()

# Sidebar
st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Choose an option",
    ["Dashboard", "Add Expense", "View Expenses", "Delete Expense"]
)

# Dashboard
if menu == "Dashboard":

    st.subheader("📊 Expense Dashboard")

    if not df.empty:
        st.subheader("Expense Category Summary")

        category_data = df.groupby("category")["amount"].sum()

        st.bar_chart(category_data)

        st.subheader("Recent Transactions")
        st.dataframe(df, use_container_width=True)

    else:
        st.info("No expenses available. Add your first expense!")

# Add expense
elif menu == "Add Expense":

    st.subheader("➕ Add New Expense")

    with st.form("expense_form"):

        title = st.text_input("Expense Name")

        amount = st.number_input(
            "Expense Amount (₹)",
            min_value=0.01,
            step=1.0
        )

        category = st.selectbox(
            "Select Category",
            ["Food", "Travel", "Shopping", "Education", "Bills", "Other"]
        )

        submit = st.form_submit_button("Add Expense")

        if submit:

            if title.strip():

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO expenses (title, amount, category)
                    VALUES (?, ?, ?)
                """, (title.strip(), amount, category))

                conn.commit()
                conn.close()

                st.success("Expense added successfully! 🎉")
                st.rerun()

            else:
                st.error("Please enter an expense name.")

# View expenses
elif menu == "View Expenses":

    st.subheader("📋 All Transactions")

    if not df.empty:
        st.dataframe(df, use_container_width=True)

    else:
        st.warning("No expenses found!")

# Delete expense
elif menu == "Delete Expense":

    st.subheader("🗑️ Delete Expense")

    if not df.empty:

        expense_id = st.selectbox(
            "Select Expense ID",
            df["id"].tolist()
        )

        if st.button("Delete Selected Expense"):

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM expenses WHERE id = ?",
                (int(expense_id),)
            )

            conn.commit()
            conn.close()

            st.success("Expense deleted successfully!")
            st.rerun()

    else:
        st.info("No expenses available to delete.")

# Footer
st.divider()
st.caption("Personal Expense Tracker | Developed using Python, SQLite and Streamlit")
