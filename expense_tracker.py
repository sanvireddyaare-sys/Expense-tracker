import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

FILENAME = "expenses.csv"

def initialize_file():
    try:
        with open(FILENAME, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])
    except FileExistsError:
        pass

def add_expense():
    date = input("Date (YYYY-MM-DD) [Enter for today]: ") or datetime.today().strftime('%Y-%m-%d')
    category = input("Category: ")
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Invalid amount.")
        return
    description = input("Description: ")

    with open(FILENAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])
    print("✅ Expense added.")

def view_expenses(filter_by=None, value=None):
    try:
        with open(FILENAME, newline="") as file:
            reader = csv.DictReader(file)
            total = 0
            filtered = []

            for row in reader:
                if filter_by == "month":
                    if not row["Date"].startswith(value):
                        continue
                elif filter_by == "category":
                    if row["Category"].lower() != value.lower():
                        continue

                filtered.append(row)
                total += float(row["Amount"])

            if not filtered:
                print("No matching records.")
                return

            print("\nDate       | Category     | Amount    | Description")
            print("-" * 60)
            for row in filtered:
                print(f"{row['Date']:10} | {row['Category']:12} | ${float(row['Amount']):8.2f} | {row['Description']}")
            print("-" * 60)
            print(f"Total: ${total:.2f}")
    except FileNotFoundError:
        print("No data yet.")

def show_pie_chart():
    try:
        with open(FILENAME, newline="") as file:
            reader = csv.DictReader(file)
            category_totals = defaultdict(float)

            for row in reader:
                category_totals[row["Category"]] += float(row["Amount"])

            if not category_totals:
                print("No data to plot.")
                return

            labels = list(category_totals.keys())
            sizes = list(category_totals.values())

            plt.figure(figsize=(6, 6))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.title("Expenses by Category")
            plt.axis('equal')
            plt.show()
    except FileNotFoundError:
        print("No data yet.")

def show_bar_chart():
    try:
        with open(FILENAME, newline="") as file:
            reader = csv.DictReader(file)
            daily_totals = defaultdict(float)

            for row in reader:
                daily_totals[row["Date"]] += float(row["Amount"])

            if not daily_totals:
                print("No data to plot.")
                return

            dates = sorted(daily_totals.keys())
            amounts = [daily_totals[date] for date in dates]

            plt.figure(figsize=(10, 5))
            plt.bar(dates, amounts, color='skyblue')
            plt.xticks(rotation=45)
            plt.title("Expenses by Date")
            plt.xlabel("Date")
            plt.ylabel("Amount ($)")
            plt.tight_layout()
            plt.show()
    except FileNotFoundError:
        print("No data yet.")

def main():
    initialize_file()
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Filter by Month (e.g. 2025-04)")
        print("4. Filter by Category")
        print("5. Show Pie Chart (by Category)")
        print("6. Show Bar Chart (by Date)")
        print("7. Quit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            month = input("Enter month (YYYY-MM): ")
            view_expenses(filter_by="month", value=month)
        elif choice == "4":
            category = input("Enter category: ")
            view_expenses(filter_by="category", value=category)
        elif choice == "5":
            show_pie_chart()
        elif choice == "6":
            show_bar_chart()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
