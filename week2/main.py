#!/usr/bin/env python3

from pathlib import Path
import csv
import json

file_input_data = Path("./data") / "week2_dataset_expenses_raw.csv"
file_input_category_mapping = Path("./data") / "week2_dataset_category_mapping.json"
file_output_clean_data = Path("./output") / "clean_expenses.csv"

def write_to_csv_file(valid_rows):
    try:
        with open(file_output_clean_data, "w", newline="", encoding="utf-8") as file:
            fieldnames = ['date', 'category', 'description', 'amount', 'payment_method', \
                          'currency', 'merchant', 'city']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(valid_rows)
    except OSError as e:
        print(e)
        print("Failed to save the cleaned input. Exiting program.")
        exit()

def clean_text(text, *payment_method):
    if not payment_method:
        mod_text = " ".join(text.split())
        if mod_text.isupper():
            # Don't .title() a merchant uses all uppercases
            return mod_text
        return mod_text.title()

    return " ".join(text.split(sep="_")).title()

def standardize_categories(data):
    try:
        with open(file_input_category_mapping, "r", encoding="utf-8") as file:
            content = json.load(file)
            for row in data:
                category = row['category'].lower()
                for item, key in content.items():
                    if category == item:
                        # print(category, "-", key)
                        row['category'] = key
    except OSError as e:
        print(e)
        print("Can not perform standardization of categories")
    return data

def print_summary(num_valid_rows, num_invalid_rows):
    print("=" * 40)
    print(f"Summary of cleaned {file_input_data} file:\n")
    print(f"\t{num_valid_rows} valid rows")
    print(f"\t{num_invalid_rows} invalid rows")
    print(f"\nWritten to {file_output_clean_data}")
    print("=" * 40)

def read_expenses():
    valid_rows = []
    num_valid_rows = 0
    num_invalid_rows = 0
    try:
        with open(file_input_data, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    # Handle text fields first
                    date = row['date']
                    category = clean_text(row['category'])
                    description = clean_text(row['description'])
                    if not date or not category or not description:
                        raise ValueError('Missing text field')

                    payment_method = row['payment_method']
                    currency = row['currency'].capitalize()
                    merchant = clean_text(row['merchant'])
                    city = row['city']
                    if not payment_method or not currency or not merchant or not city:
                        raise ValueError('Missing text field')

                    payment_method = clean_text(payment_method, True)

                    # Handle number fields
                    if row['amount'].isalpha() or row['amount'] == "" or float(row['amount']) <= 0.00:
                        raise ValueError('Invalid number')

                    amount = float(row['amount'])

                    valid_rows.append({
                        "date": date,
                        "category": category,
                        "description": description,
                        "amount": amount,
                        "payment_method": payment_method,
                        "currency": currency,
                        "merchant": merchant,
                        "city": city,
                    })

                    num_valid_rows += 1

                except (ValueError, KeyError) as e:
                    # Log errors
                    # print(e)
                    num_invalid_rows += 1
    except OSError as e:
        print(e)
        print("Exiting program.")
        exit()

    return [valid_rows, num_valid_rows, num_invalid_rows]

if __name__ == '__main__':
    valid_rows, num_valid_rows, num_invalid_rows = read_expenses()
    valid_rows = standardize_categories(valid_rows)

    write_to_csv_file(valid_rows)
    print_summary(num_valid_rows, num_invalid_rows)
