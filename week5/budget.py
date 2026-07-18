#!/usr/bin/env python3


class Budget:
    """Manages the budget data, updates data and performs calculations on the data"""

    def __init__(self, df, base_currency):
        self.df = df
        self.base_currency = base_currency

    def update_from_eur_to_base(self, conversion):
        eur_expenses = self.df.get("currency").eq("EUR")
        idx_eur_expenses = eur_expenses[eur_expenses].index
        df_eur = self.df.iloc[idx_eur_expenses]

        # Converts to base currency from EUR
        for i, r in df_eur.iterrows():
            df_eur.at[i, "amount"] = conversion.convert_to_base_from_eur(r["amount"])
            df_eur.at[i, "currency"] = self.base_currency
        self.df.update(df_eur)

    def update_from_dkk_to_base(self, conversion):
        dkk_expenses = self.df.get("currency").eq("DKK")
        idx_dkk_expenses = dkk_expenses[dkk_expenses].index
        df_dkk = self.df.iloc[idx_dkk_expenses]

        # Converts to base currency from DKK
        for i, r in df_dkk.iterrows():
            df_dkk.at[i, "amount"] = conversion.convert_to_base_from_dkk(r["amount"])
            df_dkk.at[i, "currency"] = self.base_currency
        self.df.update(df_dkk)

    def total_spending_by_category(self):
        return self.df.groupby("category")["amount"].sum()

    def total_spending_by_month(self):
        return self.df.groupby("month")["amount"].sum()

    def largest_expense(self):
        largest_expense_idx = self.df["amount"].idxmax()
        largest_expense = self.df.loc[largest_expense_idx]
        return largest_expense

    def lowest_expense(self):
        lowest_expense_idx = self.df["amount"].idxmin()
        lowest_expense = self.df.loc[lowest_expense_idx]
        return lowest_expense
