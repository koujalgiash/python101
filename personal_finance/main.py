import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")  # Use TkAgg backend for interactive plotting


class CSV:
    CSV_FILE = "data/finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    # INITIALIZING CSV FILE
    # for more explanation on try and except statements, check notes and tips.
    @classmethod
    def initialze_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    # CREATING A NEW DICTIONARY WITH ALL THE DATA THAT NEED TO BE ADDED INTO THE CSV FILE
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }

        # OPENED A CSV FILE IN APPEND MODE
        #'with' syntax is a "context manager" that allows us to do anything within the 'with' block and automatically handles closing the file.
        with open(
            cls.CSV_FILE, "a", newline=""
        ) as csvfile:  #'csvfile' is a variable to store open file
            writer = csv.DictWriter(
                csvfile, fieldnames=cls.COLUMNS
            )  #'csv.DictWriter' takes a dictionary and writes it into the csv file
            writer.writerow(new_entry)
        print("Entry added successfully")

    # TO SUMMARIZE ALL TRANSCATIONS AND PREPARE FOR VISUALIZATION.
    # GETS ALL THE TRANSACTIONS WITHIN A DATE RANGE
    # convert all the dates inside of the date column into a datetime object. Use them to filter by different transactions.
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(
            df["date"], format=CSV.FORMAT, errors="coerce"
        )  # create a "FORMAT" variable to avoid repetition, find it in the csv class
        df = df.dropna(subset=["date"])
        start_date = datetime.strptime(
            start_date, CSV.FORMAT
        )  # the start date entered by the user will be a string so we
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        # "mask" is a filtering boolean condition used to index, filter, or modify data
        # It can be applied to the different rows inside of a dataframe to see if we should select that row or not.
        # '&' is similar to "and" operator, but used specifically when working with a pandas dataframe or mask.
        # "formatters" are tools used to control the formatting of output
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]  # only returns the rows that matches the mask.

        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(
                f"Transctions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )
            # date is the python dictionary, column_name is the key. Applies a function to every single element inside the column if we want to format it differently
            # all the date entries are passed through the lambda function. X is a datetime object obtained from df date and converted to string format

            total_income = filtered_df[filtered_df["category"] == "Income"][
                "amount"
            ].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"][
                "amount"
            ].sum()
            # getting all the rows where the catergory is income/expense, from those rows, get the amount and sum
            print("\nSummary:")
            print(
                f"Total Income: €{total_income:.2f}"
            )  # .2f formats to two decimal places.
            print(f"Total Expense: €{total_expense:.2f}")
            print(f"Net Savings: €{(total_income - total_expense):.2f}")

        return filtered_df


# WRITE A FUNCTION THAT WILL CALL THE FUNCTIONS FROM 'data_entry.py' IN A DESIRED ORDER REQUIRED FOR DATA COLLECTION
def add():
    CSV.initialze_csv()
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ",
        allow_default=True,
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


# Calls the function which adds new entries.
# add()

# Calls the function to display all transactions within the date range along with a summary.
# CSV.get_transactions("01-01-2025", "31-05-2025")


# Plotting
def plot_transactions(df):
    df.set_index("date", inplace=True)

    # To fill in missing dates and add continuity to graph line, we create new dataframes for income and expenses.
    income_df = (
        df[df["category"] == "Income"]
        .resample(
            "D"
        )  #'D' is daily frequency, 'resample' adds a row for every single day
        .sum()  # 'sum' to aggregate different values which are on the same day.
        .reindex(df.index, fill_value=0)  # Marking empty days as 0
        .sort_index()
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
        .sort_index()
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


# Defining a function to interact at the terminal for a smoother use of adding, viewing and summarizing transactions.
def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")


# if we run this main.py file directly, the if statement below will execute and call the main() function
if __name__ == "__main__":
    main()
