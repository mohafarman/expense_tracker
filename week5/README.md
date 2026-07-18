## Week 5, Final Project

Expense Tracker is a project I built during the Applied Programming with Python course DA667A at Kristianstad University. Using data about expenses in a csv format and accepting budget targets as well as different exchange rates this program creates a summary of the expenses. It handles currency conversion, compares expenses to budget and looks at spending based on category and month. It also generates charts for visual data representation and outputs a report and csv files as summaries.

### How to run

``` sh
python main.py
```

### Project structure:
.
├── budget.py
├── currency.py
├── data
│   ├── week4_dataset_test_cases.csv
│   ├── week5_dataset_budget_targets.json
│   ├── week5_dataset_exchange_rates_sample.json
│   └── week5_dataset_expenses_final.csv
├── main.py
├── output
│   ├── category_chart.png
│   ├── category_summary.csv
│   ├── finance_report.txt
│   ├── month_chart.png
│   └── month_summary.csv
├── output.png
├── README.txt
└── tests
    └── test_project.py

4 directories, 15 files
