# THIS FILE WAS CREATED TO CONTAIN ALL THE FUNCTIONS RELATED TO GETTING NFORMATION FROM THE USER
# i.e. TO MAKE THE PROCESS OF DATA ENTRY EASIER and to keep the main.py file clean and organised

# IMPORTING ALL THE FUNCTIONS ON MAIN.PY FILE
from datetime import datetime

# 'prompt' asks the user to input before they give us the date, in a situation with multiple date entries at different times
# 'allow_default' tells us if we should have a default value of today's date. And avoid making the user enter today's date.
date_format = "%d-%m-%Y"  # creare a variable date format to avoid repetition and make easy changes


def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(
            date_format
        )  # to covert the input date into a string format and convert into required format

    # to clean up the date user types in and gives it into the format that user needs
    # for more explanation on try and except statements, check notes and tips.
    try:
        valid_date = datetime.strptime(
            date_str, date_format
        )  # to convert any invalid date entry and convert into required format
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format.")
        return get_date(prompt, allow_default)


def get_amount():
    try:
        amount = float(
            input("Enter the amount: ")
        )  # to convert the variable type into float incase the amount is in decimal
        if amount <= 0:
            raise ValueError("Amount must be a non-negative non-zero value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()


CATEGORIES = {"I": "Income", "E": "Expense"}  # defining a dictonary for categories


def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]  # referring to the key within the dictionary.

    print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")
    return get_category()


def get_description():
    return input("Enter a description (optional): ")
