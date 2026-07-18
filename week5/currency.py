#!/usr/bin/env python3

from pathlib import Path
import json


class Currency:
    """Handles the currencies and conversion from an input json file"""

    def __init__(self):
        self.base_currency = ""
        # ZeroDivisionError if exchange rates not loaded
        self.currency_rate_eur = 0
        self.currency_rate_dkk = 0

    def load_exchange_rates(self, file_path):
        try:
            with open(file_path, "r") as file:
                currency_rates = json.load(file)
                self.base_currency = currency_rates["base"]
                self.currency_rate_eur = currency_rates["rates"]["EUR"]
                self.currency_rate_dkk = currency_rates["rates"]["DKK"]
        except OSError as e:
            print(e)
            print("Failed to load exchange rates")

    def convert_to_base_from_eur(self, amount):
        # Will return ZeroDivisionError if exchange rate not set
        try:
            conversion = amount / self.currency_rate_eur
            formatted_conversion = f"{conversion:.3f}"
            return float(formatted_conversion)
        except ZeroDivisionError as e:
            raise e

    def convert_to_base_from_dkk(self, amount):
        # Will return ZeroDivisionError if exchange rate not set
        try:
            conversion = amount / self.currency_rate_dkk
            formatted_conversion = f"{conversion:.3f}"
            return float(formatted_conversion)
        except ZeroDivisionError as e:
            raise e
