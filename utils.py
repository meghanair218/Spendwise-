
import re
from datetime import datetime


class InvalidInputError(Exception):
    pass


def validate_date(date_text):
    pattern = r"^\d{4}-\d{2}-\d{2}$"

    if not re.fullmatch(pattern, date_text):
        return False

    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_expense_id(expense_id):
    return bool(re.fullmatch(r"EXP-[0-9]{3}", expense_id))


def parse_tags(tag_text):
    return {
        tag.strip().lower()
        for tag in tag_text.split(",")
        if tag.strip()
    }
