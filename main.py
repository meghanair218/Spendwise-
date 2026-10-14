
from datetime import date
from models import Expense, ExpenseTracker
from storage import save_to_json, load_from_json
from utils import validate_date, parse_tags

FILENAME = "expenses.json"


def display_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return

    print("\n" + "-" * 75)
    print(f"{'ID':<10} {'DATE':<12} {'CATEGORY':<15} {'AMOUNT':>12}")
    print("-" * 75)

    for expense in expenses:
        print(
            f"{expense.expense_id:<10} "
            f"{expense.date:<12} "
            f"{expense.category:<15} "
            f"₹{expense.amount:>10.2f}"
        )
        print(f"  Tags: {', '.join(sorted(expense.tags)) or 'none'}")

    print("-" * 75)


def add_new_expense(tracker):
    try:
        expense_date = input(
            "Enter date (YYYY-MM-DD), or press Enter for today: "
        ).strip()

        if not expense_date:
            expense_date = date.today().isoformat()

        if not validate_date(expense_date):
            print("Invalid date. Use a valid YYYY-MM-DD date.")
            return

        category = input("Enter category: ").strip()

        if not category:
            print("Category cannot be empty.")
            return

        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        tag_text = input("Enter tags separated by commas: ")
        tags = parse_tags(tag_text)

        expense_id = f"EXP-{len(tracker.expenses) + 1:03d}"

        expense = Expense(
            expense_id, expense_date, category, amount, tags
        )

        tracker.add_expense(expense)
        print("\nExpense added successfully!")
        print(expense)

        if tracker.is_over_budget():
            print("Warning: You have exceeded your budget!")
        elif tracker.get_total_spending() >= tracker.budget_limit:
            print("You have reached your budget limit.")
        else:
            print("You are within your budget.")

    except ValueError:
        print("Invalid amount. Please enter a valid number.")


def show_category_summary(tracker):
    summary = tracker.get_category_summary()

    if not summary:
        print("No expenses available.")
        return

    print("\n--- Category Summary ---")
    for category, total in summary.items():
        print(f"{category}: ₹{total:.2f}")


def search_by_category(tracker):
    category = input("Enter category to search: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    results = tracker.filter_by_category(category)
    display_expenses(results)


def main():
    expenses = load_from_json(FILENAME)

    try:
        budget = float(input("Enter your total spending budget: "))

        if budget < 0:
            print("Budget cannot be negative. Using zero.")
            budget = 0.0

    except ValueError:
        print("Invalid budget. Using zero.")
        budget = 0.0

    tracker = ExpenseTracker(expenses, budget)

    print("\nWelcome to SpendWise CLI!")

    while True:
        print("\n========== SPENDWISE ==========")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Category Summary")
        print("4. Search by Category")
        print("5. Save and Exit")
        # print("6. View Expenses Sorted by Amount")
        # print("7. View Total Spending")
        print("================================")

        choice = input("Enter your choice: ").strip()

        match choice:
            case "1":
                add_new_expense(tracker)

            case "2":
                display_expenses(tracker.expenses)

            case "3":
                show_category_summary(tracker)

            case "4":
                search_by_category(tracker)

            case "5" | "exit":
                save_to_json(FILENAME, tracker.expenses)
                print("Thank you for using SpendWise!")
                break

            # case "6":
            #     display_expenses(tracker.sort_by_amount())

            # case "7":
            #     count, total = tracker.get_summary()
            #     print(f"Number of expenses: {count}")
            #     print(f"Total spending: ₹{total:.2f}")

            case _:
                print("Invalid option. Please choose 1 to 7.")


if __name__ == "__main__":
    main()
