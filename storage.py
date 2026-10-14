
import json
from models import Expense


def save_to_json(filename, expenses_list):
    try:
        data = [expense.to_dict() for expense in expenses_list]

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print("Expenses saved successfully!")

    except OSError as error:
        print(f"Error saving expenses: {error}")


def load_from_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            print("Invalid JSON format. Starting with empty records.")
            return []

        return [Expense.from_dict(item) for item in data]

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("JSON file is empty or corrupted. Starting with empty records.")
        return []

    except (ValueError, KeyError, TypeError) as error:
        print(f"Invalid expense data: {error}")
        return []
