import datetime
import json
import os

class Expense:
    def __init__(self, amount, category, description):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class ExpenseTracker:
    def __init__(self, data_file="expenses.json"):
        self.data_file = data_file
        self.expenses = []
        self.load_expenses()

    def load_expenses(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    self.expenses = [Expense(**expense) for expense in json.load(file)]
            except json.JSONDecodeError:
                print("Error loading data. The file might be corrupted.")
        else:
            self.expenses = []

    def save_expenses(self):
        try:
            with open(self.data_file, 'w') as file:
                json.dump([expense.__dict__ for expense in self.expenses], file)
        except IOError as e:
            print(f"Error saving data: {e}")

    def add_expense(self, amount, category, description):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount should be greater than zero.")
        except ValueError as e:
            print(f"Invalid amount: {e}")
            return

        expense = Expense(amount, category, description)
        self.expenses.append(expense)
        self.save_expenses()
        print("Expense added successfully!")

    def view_expenses(self):
        if not self.expenses:
            print("No expenses recorded.")
            return

        for i, expense in enumerate(self.expenses, 1):
            print(f"{i}. {expense.date} - {expense.category}: ${expense.amount} - {expense.description}")

    def total_expenses(self):
        total = sum(expense.amount for expense in self.expenses)
        print(f"Total Expenses: ${total:.2f}")

    def filter_by_category(self, category):
        filtered_expenses = [expense for expense in self.expenses if expense.category.lower() == category.lower()]
        if not filtered_expenses:
            print(f"No expenses found in the '{category}' category.")
            return

        for i, expense in enumerate(filtered_expenses, 1):
            print(f"{i}. {expense.date} - {expense.category}: ${expense.amount} - {expense.description}")

    def monthly_summary(self):
        summary = {}
        for expense in self.expenses:
            month_year = expense.date[:7]  # Get YYYY-MM part of the date
            if month_year not in summary:
                summary[month_year] = 0
            summary[month_year] += expense.amount

        for month_year, total in summary.items():
            print(f"{month_year}: ${total:.2f}")

    def category_summary(self):
        summary = {}
        for expense in self.expenses:
            if expense.category not in summary:
                summary[expense.category] = 0
            summary[expense.category] += expense.amount

        for category, total in summary.items():
            print(f"{category}: ${total:.2f}")


def main():
    tracker = ExpenseTracker()

    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Total Expenses")
        print("4. Filter Expenses by Category")
        print("5. Monthly Expense Summary")
        print("6. Category-wise Expense Summary")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            amount = input("Enter the amount: ")
            category = input("Enter the category (e.g., food, transportation, entertainment): ")
            description = input("Enter a description: ")
            tracker.add_expense(amount, category, description)
        elif choice == '2':
            tracker.view_expenses()
        elif choice == '3':
            tracker.total_expenses()
        elif choice == '4':
            category = input("Enter the category to filter by: ")
            tracker.filter_by_category(category)
        elif choice == '5':
            tracker.monthly_summary()
        elif choice == '6':
            tracker.category_summary()
        elif choice == '7':
            print("Exiting the Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

