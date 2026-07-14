#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import json
import os

file_input_clean_data = Path("./data") / "week3_dataset_expenses_cleaned.csv"
file_input_exchange_rates = Path("./data") / "week3_dataset_exchange_rates_sample.json"
file_input_budget_targets = Path("./data") / "week3_dataset_budget_targets.json"
folder_output_path = Path("./output")
file_output_month_chart = Path("./output") / "month_chart.png"
file_output_category_chart = Path("./output") / "category_chart.png"
file_output_month_summary = Path("./output") / "month_summary.csv"
file_output_category_summary = Path("./output") / "category_summary.csv"


def create_output_folder():
    if not os.path.exists(folder_output_path):
        os.makedirs(folder_output_path)


def find_largest_expense(df):
    largest_expense_idx = df["amount"].idxmax()
    largest_expense = df.loc[largest_expense_idx]
    return largest_expense


def get_total_spending_by_category(df):
    return df.groupby("category")["amount"].sum()


def get_total_spending_by_month(df):
    return df.groupby("month")["amount"].sum()


def create_month_chart(total_spending):
    """Line chart"""
    plt.plot(total_spending.keys(), total_spending.values, marker="o")
    plt.title("Total spending by month")
    plt.xlabel("Months")
    plt.ylabel("SEK")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(file_output_month_chart)
    # plt.show()
    return


def create_category_chart(total_spending, budget_targets):
    """Bar chart, compares to budget target"""

    budget = {
        "Total Spending": total_spending.values,
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
    ax.set_ylabel("SEK")
    ax.legend(loc="upper left", ncols=2)
    plt.savefig(file_output_category_chart)
    plt.show()
    return


def currency_converter(df):
    """
    SEK amounts stay the same.
    EUR amounts should be converted to SEK by dividing by 0.088.
    DKK amounts should be converted to SEK by dividing by 0.65.
    """
    currency_rate_eur = 0
    dkk_rate = 0
    try:
        with open(file_input_exchange_rates, "r") as file:
            currency_rates = json.load(file)
            currency_base = currency_rates["base"]
            currency_rate_eur = currency_rates["rates"]["EUR"]
            currency_rate_dkk = currency_rates["rates"]["DKK"]
    except OSError as e:
        print(e)
        exit()

    # Get all the rows with other currencies than SEK
    eur_expenses = df.get("currency").eq("EUR")
    idx_eur_expenses = eur_expenses[eur_expenses].index
    df_eur = df.iloc[idx_eur_expenses]

    dkk_expenses = df.get("currency").eq("DKK")
    idx_dkk_expenses = dkk_expenses[dkk_expenses].index
    df_dkk = df.iloc[idx_dkk_expenses]

    # Converts to SEK from EUR
    for i, r in df_eur.iterrows():
        conversion = r["amount"] / currency_rate_eur
        formatted_conversion = f"{conversion:.3f}"
        df_eur.at[i, "amount"] = float(formatted_conversion)
        df_eur.at[i, "currency"] = currency_base

    # Converts to SEK from DKK
    for i, r in df_dkk.iterrows():
        conversion = r["amount"] / currency_rate_dkk
        formatted_conversion = f"{conversion:.2f}"
        df_dkk.at[i, "amount"] = float(formatted_conversion)
        df_dkk.at[i, "currency"] = currency_base

    # Update the respective columns
    df.update(df_eur)
    df.update(df_dkk)


def print_summary():
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

            # convert curr to SEK before analysing, comparing and outputting
            currency_converter(df)

            total_spending_by_category = get_total_spending_by_category(df)
            total_spending_by_month = get_total_spending_by_month(df)
            largest_expense = find_largest_expense(df)

            # Create charts and save them
            create_category_chart(total_spending_by_category, budget_targets)
            plt.figure()
            create_month_chart(total_spending_by_month)

            # Generate category and month summary csv files
            total_spending_by_category.to_csv(file_output_category_summary)
            total_spending_by_month.to_csv(file_output_month_summary)
    except OSError as e:
        print(e)
        exit()

    print_summary()
