import sqlite3
from datetime import datetime

# Connect or create database
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
""")
conn.commit()

def add_expense():
    date = datetime.now().strftime("%Y-%m-%d")
    category = input("Enter category (Food, Transport, Bills, etc): ")
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")

    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                   (date, category, amount, description))
    conn.commit()
    print("✅ Expense added successfully!\n")

def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    print(f"\n{'ID':<5}{'Date':<12}{'Category':<15}{'Amount':<10}{'Description'}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<5}{row[1]:<12}{row[2]:<15}{row[3]:<10}{row[4]}")
    print()

def category_summary():
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    rows = cursor.fetchall()

    print("\n💰 Category-wise Spending:")
    print("-" * 30)
    for category, total in rows:
        print(f"{category:<15} ₹{total:.2f}")
    print()

def monthly_report():
    month = input("Enter month (YYYY-MM): ")
    cursor.execute("SELECT date, category, amount, description FROM expenses WHERE date LIKE ?", (f"{month}%",))
    rows = cursor.fetchall()

    total = 0
    print(f"\n📅 Expenses for {month}:")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]} - {row[1]} - ₹{row[2]} - {row[3]}")
        total += row[2]
    print(f"\nTotal Spending in {month}: ₹{total:.2f}\n")

def main():
    while True:
        print("===== Expense Tracker =====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Category Summary")
        print("4. Monthly Report")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            category_summary()
        elif choice == '4':
            monthly_report()
        elif choice == '5':
            print("👋 Exiting Expense Tracker. Bye!")
            break
        else:
            print("Invalid choice. Try again!\n")

if __name__ == "__main__":
    main()
    conn.close()
