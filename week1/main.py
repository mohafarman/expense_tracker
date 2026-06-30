#!/usr/bin/env python3

num_expenses = 5

def get_expenses(prompt):
    expenses = []
    for i in range(num_expenses):
        amount, category = input(prompt).rsplit(' ')
        expenses.append((int(amount), category))
    return expenses

def calculate_total(expenses):
    total_expenses = 0
    for i in range(num_expenses):
        total_expenses = total_expenses + expenses[i][0]
    return total_expenses

def calculate_average(total_expenses, expenses):
    return total_expenses / len(expenses)

def get_highest_expense(expenses):
    return max(expenses)

def print_summary(expenses):
    total_expenses = calculate_total(expenses)
    avg_expenses = calculate_average(total_expenses, expenses)
    highest_expense = get_highest_expense(expenses)

    print("\n" + "=" * 40)
    print("Expense Tracker")

    print("\nSummary:")
    print(f"Total expenses:\t\t\t{total_expenses:>8.2f} kr")
    print(f"Average expenses:\t\t{avg_expenses:>8.2f} kr")
    print(f"Highest expense ({highest_expense[1]}):\t{highest_expense[0]:>8.2f} kr")

if __name__ == '__main__':
    print("Track your expenses")
    expenses = get_expenses('Enter expenses and category, seperated by a space: ')
    print_summary(expenses)
