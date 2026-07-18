#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from budget import Budget
from currency import Currency
import json
import os

file_input_data = Path("./data") / "week5_dataset_expenses_final.csv"
file_input_budget_targets = Path("./data") / "week5_dataset_budget_targets.json"
file_input_exchange_rates = Path("./data") / "week5_dataset_exchange_rates_sample.json"
folder_output_path = Path("./output")
file_output_month_chart = Path("./output") / "month_chart.png"
file_output_category_chart = Path("./output") / "category_chart.png"
file_output_month_summary = Path("./output") / "month_summary.csv"
file_output_category_summary = Path("./output") / "category_summary.csv"
file_output_finance_report = Path("./output") / "finance_report.txt"


def create_output_folder():
    """Creates the output folder if it does not already exist"""
    if not os.path.exists(folder_output_path):
        os.makedirs(folder_output_path)


def create_category_chart(total_spending, budget_targets, currency):
    """Creates and saves category chart comparing to budget targets into output folder"""

    budget = {
        "Total Spending": total_spending,
        "Budget Target": budget_targets.values(),
    }
    _, ax = plt.subplots()
    ax.grouped_bar(
        budget,
        tick_labels=[
            "Food",
            "Transport",
            "Bills",
            "Entertainment",
            "Health",
            "Shopping",
            "Study",
            "Travel",
            "Household",
        ],
    )
    ax.set_title("Total spending by category")
    ax.set_xlabel("Categories")
    ax.set_ylabel(currency)
    ax.legend(loc="upper left", ncols=2)
    plt.savefig(file_output_category_chart)
    return


def create_month_chart(total_spending):
    """Creates and saves month chart into output folder"""
    plt.plot(total_spending.keys(), total_spending.values, marker="o")
    plt.title("Total spending by month")
    plt.xlabel("Months")
    plt.ylabel("SEK")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(file_output_month_chart)
    return


def print_report(
    spending_by_category,
    spending_by_month,
    largest_expense,
    lowest_expense,
    budget_targets,
    currency,
):
    """Prints out a summary report of our expense tracker and save the output to a text file"""
    total_expenses = spending_by_month.sum()
    avg_monthly_expenses = spending_by_month.mean()
    largest_expense_amount = largest_expense.iloc[3]
    largest_expense_description = largest_expense.iloc[2]
    largest_expense_date = largest_expense.iloc[0]

    lowest_expense_amount = lowest_expense.iloc[3]
    lowest_expense_description = lowest_expense.iloc[2]
    lowest_expense_date = lowest_expense.iloc[0]

    print("=" * 40)
    print("Expense Tracker")
    print(
        f"Analysis of data from {file_input_data} compared to budget targets from {file_input_budget_targets}"
    )
    print("\nSummary:")
    print(f"Total expenses:\t\t{total_expenses:>8.2f} {currency}")
    print(
        f"Most expensive expense happened {largest_expense_date} and costed you {largest_expense_amount} {currency} which was a {largest_expense_description.lower()}."
    )
    print(
        f"Most cheapest expense happened {lowest_expense_date} and costed you {lowest_expense_amount} {currency} which was a {lowest_expense_description.lower()}."
    )
    print(f"Spending by month:")

    for month, amount in spending_by_month.items():
        print(f"\t{month}\t\t{amount:.2f} {currency}")

    print(
        f"\nWhich is an average expending of {avg_monthly_expenses:.2f} {currency} every month"
    )

    print(f"\nSpending by category:")
    for category, amount in spending_by_category.items():
        if len(category) >= 7:
            print(f"\t{category}\t{amount:.2f} {currency}")
        else:
            print(f"\t{category}\t\t{amount:.2f} {currency}")

    print(
        f"\nSummary chart and csv of spending by category written to:\n\t{file_output_category_chart} and {file_output_category_summary}"
    )
    print(
        f"Summary chart csv of spending by month written to\n\t{file_output_month_chart} and {file_output_month_summary}"
    )
    print("=" * 40)

    try:
        with open(file_output_finance_report, "w") as txt_file:
            print("=" * 40, file=txt_file)
            print("Expense Tracker", file=txt_file)
            print(
                f"Analysis of data from {file_input_data} compared to budget targets from {file_input_budget_targets}",
                file=txt_file,
            )
            print("\nSummary:", file=txt_file)
            print(
                f"Total expenses:\t\t{total_expenses:>8.2f} {currency}", file=txt_file
            )
            print(
                f"Most expensive expense happened {largest_expense_date} and costed you {largest_expense_amount} {currency} which was a {largest_expense_description.lower()}.",
                file=txt_file,
            )
            print(
                f"Most cheapest expense happened {lowest_expense_date} and costed you {lowest_expense_amount} {currency} which was a {lowest_expense_description.lower()}.",
                file=txt_file,
            )
            print(f"Spending by month:", file=txt_file)

            for month, amount in spending_by_month.items():
                print(f"\t{month}\t\t{amount:.2f} {currency}", file=txt_file)

            print(
                f"\nWhich is an average expending of {avg_monthly_expenses:.2f} {currency} every month",
                file=txt_file,
            )

            print(f"\nSpending by category:", file=txt_file)
            for category, amount in spending_by_category.items():
                if len(category) >= 7:
                    print(f"\t{category}\t{amount:.2f} {currency}", file=txt_file)
                else:
                    print(f"\t{category}\t\t{amount:.2f} {currency}", file=txt_file)

            print(
                f"\nSummary chart and csv of spending by category written to:\n\t{file_output_category_chart} and {file_output_category_summary}",
                file=txt_file,
            )
            print(
                f"Summary chart csv of spending by month written to\n\t{file_output_month_chart} and {file_output_month_summary}",
                file=txt_file,
            )
            print("=" * 40, file=txt_file)
        print(f"\nSummary report written to {file_output_finance_report}")
    except OSError as e:
        print(f"Finance report could not be written to {file_output_finance_report}.")


def print_report_to_console(
    spending_by_category,
    spending_by_month,
    largest_expense,
    lowest_expense,
    budget_targets,
    currency,
):
    """Prints out a summary report of the budget, as well as of the input and output files to the console"""
    total_expenses = spending_by_month.sum()
    avg_monthly_expenses = spending_by_month.mean()
    largest_expense_amount = largest_expense.iloc[3]
    largest_expense_description = largest_expense.iloc[2]
    largest_expense_date = largest_expense.iloc[0]

    lowest_expense_amount = lowest_expense.iloc[3]
    lowest_expense_description = lowest_expense.iloc[2]
    lowest_expense_date = lowest_expense.iloc[0]

    print("=" * 40)
    print("Expense Tracker")
    print(
        f"Analysis of data from {file_input_data} compared to budget targets from {file_input_budget_targets}"
    )
    print("\nSummary:")
    print(f"Total expenses:\t\t{total_expenses:>8.2f} {currency}")
    print(
        f"Most expensive expense happened {largest_expense_date} and costed you {largest_expense_amount} {currency} which was a {largest_expense_description.lower()}."
    )
    print(
        f"Most cheapest expense happened {lowest_expense_date} and costed you {lowest_expense_amount} {currency} which was a {lowest_expense_description.lower()}."
    )
    print(f"Spending by month:")

    for month, amount in spending_by_month.items():
        print(f"\t{month}\t\t{amount:.2f} {currency}")

    print(
        f"\nWhich is an average expending of {avg_monthly_expenses:.2f} {currency} every month"
    )

    print(f"\nSpending by category:")
    for category, amount in spending_by_category.items():
        if len(category) >= 7:
            print(f"\t{category}\t{amount:.2f} {currency}")
        else:
            print(f"\t{category}\t\t{amount:.2f} {currency}")

    print(
        f"\nSummary chart and csv of spending by category written to:\n\t{file_output_category_chart} and {file_output_category_summary}"
    )
    print(
        f"Summary chart csv of spending by month written to\n\t{file_output_month_chart} and {file_output_month_summary}"
    )
    print("=" * 40)


if __name__ == "__main__":
    budget_targets = ""
    try:
        with open(file_input_budget_targets, "r") as file:
            budget_targets = json.load(file)
    except OSError as e:
        print(e)
        exit()

    try:
        with open(file_input_data, "r") as file:
            df = pd.read_csv(file)

            create_output_folder()
            budget = Budget(df, "SEK")
            currency_handler = Currency()
            currency_handler.load_exchange_rates(file_input_exchange_rates)

            # convert currency to base currency before analysing, comparing and outputting
            budget.update_from_eur_to_base(currency_handler)
            budget.update_from_dkk_to_base(currency_handler)

            total_spending_by_category = budget.total_spending_by_category()
            total_spending_by_month = budget.total_spending_by_month()
            largest_expense = budget.largest_expense()
            lowest_expense = budget.lowest_expense()

            # Create charts and save them
            create_category_chart(
                total_spending_by_category, budget_targets, budget.base_currency
            )
            plt.figure()
            create_month_chart(total_spending_by_month)

            # Generate category and month summary csv files
            total_spending_by_category.to_csv(file_output_category_summary)
            total_spending_by_month.to_csv(file_output_month_summary)
    except OSError as e:
        print(e)
        exit()

    print_report(
        total_spending_by_category,
        total_spending_by_month,
        largest_expense,
        lowest_expense,
        budget_targets,
        budget.base_currency,
    )
