import sqlite3
import pandas as pd
from datetime import datetime

# Initialize the database
conn = sqlite3.connect("finance_tracker.db")
cursor = conn.cursor()

# Create transactions table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL, 
    category TEXT NOT NULL, 
    amount REAL NOT NULL, 
    date TEXT NOT NULL
)
''')
conn.commit()

# Function to add a transaction
def add_transaction(transaction_type, category, amount):
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO transactions (type, category, amount, date) VALUES (?, ?, ?, ?)", 
                   (transaction_type, category, amount, date))
    conn.commit()
    print(f"{transaction_type.capitalize()} of ₹{amount} added under '{category}'.")

# Function to display monthly summary
def view_summary():
    query = "SELECT type, category, SUM(amount) FROM transactions GROUP BY type, category"
    df = pd.read_sql_query(query, conn)
    if df.empty:
        print("⚠ No transactions found!")
    else:
        print("\n **Monthly Summary**")
        print(df.to_string(index=False))

# Function to view all transactions
def view_transactions():
    query = "SELECT * FROM transactions"
    df = pd.read_sql_query(query, conn)
    if df.empty:
        print("⚠ No transactions recorded yet.")
    else:
        print("\n **All Transactions**")
        print(df.to_string(index=False))

# Function to delete a transaction
def delete_transaction(transaction_id):
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    print(f"🗑 Transaction {transaction_id} deleted successfully.")

# Main loop
def main():
    while True:
        print("\n **Personal Finance Tracker**")
        print("1.Add Income")
        print("2️ Add Expense")
        print("3️ View Transactions")
        print("4️ View Summary")
        print("5️ Delete Transaction")
        print("6️ Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            category = input("Enter category (Salary, Bonus, etc.): ")
            amount = float(input("Enter amount: ₹"))
            add_transaction("income", category, amount)

        elif choice == "2":
            category = input("Enter category (Rent, Food, Entertainment, etc.): ")
            amount = float(input("Enter amount: ₹"))
            add_transaction("expense", category, amount)

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            view_summary()

        elif choice == "5":
            transaction_id = int(input("Enter transaction ID to delete: "))
            delete_transaction(transaction_id)

        elif choice == "6":
            print(" Exiting Finance Tracker. See you soon!")
            break

        else:
            print("⚠ Invalid choice! Please select a valid option.")

if __name__ == "__main__":
    main()
