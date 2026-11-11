
import sqlite3

# =====================================
# PERSONAL EXPENSE TRACKER
# =====================================

# Connect to database
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Create expenses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL
)
""")

conn.commit()


# =====================================
# 1. ADD EXPENSE
# =====================================

def add_expense():
    print("\n--- ADD NEW EXPENSE ---")

    title = input("Enter expense name: ")

    try:
        amount = float(input("Enter expense amount: "))

        if amount <= 0:
            print("Amount must be greater than zero!")
            return

    except ValueError:
        print("Please enter a valid amount!")
        return

    category = input("Enter category (Food/Travel/Shopping): ")

    cursor.execute("""
        INSERT INTO expenses (title, amount, category)
        VALUES (?, ?, ?)
    """, (title, amount, category))

    conn.commit()

    print("\nExpense added successfully!")


# =====================================
# 2. VIEW ALL EXPENSES
# =====================================

def view_expenses():
    print("\n--- ALL EXPENSES ---")

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    if expenses:
        for expense in expenses:
            print("\nID:", expense[0])
            print("Name:", expense[1])
            print("Amount: Rs.", expense[2])
            print("Category:", expense[3])
            print("----------------------")
    else:
        print("No expenses found!")


# =====================================
# 3. TOTAL EXPENSES
# =====================================

def total_expenses():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    print("\nTotal Expenses: Rs.", total or 0)


# =====================================
# 4. DELETE EXPENSE
# =====================================

def delete_expense():
    print("\n--- DELETE EXPENSE ---")

    try:
        expense_id = int(input("Enter expense ID to delete: "))
    except ValueError:
        print("Please enter a valid ID!")
        return

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()

    if cursor.rowcount > 0:
        print("\nExpense deleted successfully!")
    else:
        print("\nExpense ID not found!")


# =====================================
# MAIN MENU
# =====================================

try:
    while True:

        print("\n================================")
        print("     PERSONAL EXPENSE TRACKER")
        print("================================")

        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Total Expenses")
        print("4. Delete Expense")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            total_expenses()

        elif choice == "4":
            delete_expense()

        elif choice == "5":
            print("\nThank you for using Expense Tracker!")
            break

        else:
            print("\nInvalid choice! Please try again.")

finally:
    conn.close()
