#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from budget import Budget
from currency import Currency
import json
import os

file_input_clean_data = Path("./data") / "week4_dataset_expenses_project.csv"
file_input_budget_targets = Path("./data") / "week3_dataset_budget_targets.json"
file_input_exchange_rates = Path("./data") / "week3_dataset_exchange_rates_sample.json"
folder_output_path = Path("./output")
file_output_month_chart = Path("./output") / "month_chart.png"
file_output_category_chart = Path("./output") / "category_chart.png"
file_output_month_summary = Path("./output") / "month_summary.csv"
file_output_category_summary = Path("./output") / "category_summary.csv"


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
    # plt.show()
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
    # plt.show()
    return


def print_summary():
    """Prints out a summary of the input and output files to the console"""
    print("=" * 40)
    print(
        f"Analysis of data from {file_input_clean_data} compared to budget targets from {file_input_budget_targets}\n"
    )
    print(
        f"Summary chart and csv of spending by category written to:\n\t{file_output_category_chart} and {file_output_category_summary}"
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
        with open(file_input_clean_data, "r") as file:
            df = pd.read_csv(file)

            create_output_folder()
            budget = Budget(df, "SEK")
            currency_handler = Currency()
            currency_handler.load_exchange_rates(file_input_exchange_rates)

            # convert curr to SEK before analysing, comparing and outputting
            budget.update_from_eur_to_base(currency_handler)
            budget.update_from_dkk_to_base(currency_handler)

            total_spending_by_category = budget.total_spending_by_category()
            total_spending_by_month = budget.total_spending_by_month()
            largest_expense = budget.largest_expense()

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

    print_summary()
