#!/usr/bin/env python3

from pathlib import Path
import pandas as pd
import sys
import os

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add parent directory to sys.path
sys.path.append(parent_dir)

file_input_test_data = Path("../data") / "week4_dataset_test_cases.csv"

import unittest
from currency import Currency
from budget import Budget


class TestCurrency(unittest.TestCase):
    """Test units for the Currency class"""

    def test_convert_to_eur_from_base(self):
        c = Currency()

        # Edge case, exchange rates not set
        with self.assertRaises(ZeroDivisionError):
            c.convert_to_base_from_eur(10)
        c.currency_rate_eur = 0.088
        self.assertEqual(c.convert_to_base_from_eur(99), 1125.0)

    def test_convert_to_dkk_from_base(self):
        c = Currency()

        # Edge case, exchange rates not set
        with self.assertRaises(ZeroDivisionError):
            c.convert_to_base_from_dkk(10)
        c.currency_rate_dkk = 0.65
        self.assertEqual(c.convert_to_base_from_dkk(100), 153.846)


class TestBudget(unittest.TestCase):
    """Test units for the Budget class"""

    def test_total_spending_by_category(self):
        try:
            with open(file_input_test_data, "r") as file:
                df = pd.read_csv(file)
                budget = Budget(df, "SEK")

                category = budget.total_spending_by_category()
                bills = category["Bills"]
                food = category["Food"]
                transport = category["Transport"]
                self.assertEqual(bills, 450)
                self.assertEqual(food, 820)
                self.assertEqual(transport, 620)
        except OSError as e:
            print(e)
            exit()

    def test_total_spending_by_month(self):
        try:
            with open(file_input_test_data, "r") as file:
                df = pd.read_csv(file)
                budget = Budget(df, "SEK")

                month = budget.total_spending_by_month()
                jan = month.iloc[0]
                feb = month.iloc[1]
                self.assertEqual(jan, 1120)
                self.assertEqual(feb, 770)
        except OSError as e:
            print(e)
            exit()

    def test_largest_expense(self):
        try:
            with open(file_input_test_data, "r") as file:
                df = pd.read_csv(file)
                budget = Budget(df, "SEK")

                largest_expense_idx = df["amount"].idxmax()
                largest_expense = df.loc[largest_expense_idx]
                self.assertEqual(largest_expense["amount"], 620)
        except OSError as e:
            print(e)
            exit()


if __name__ == "__main__":
    unittest.main()
