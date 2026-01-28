import os
import pandas as pd
import logging as log
import calendar
from config import EXPORT_DIR, MODEL_DATE, MODEL_AMOUNT, MODEL_DESCRIPTION, MODEL_CATEGORY, MODEL_ORIGIN, WORK_FILE, YEAR

log.basicConfig(format="%(message)s", level=log.INFO)


# -------------------------
# Helpers
# -------------------------
def get_expenses(df):
    return df[df[MODEL_AMOUNT] < 0]


def get_income(df):
    return df[df[MODEL_AMOUNT] > 0]


# -------------------------
# Data Loading & Categorization
# -------------------------
def load_data():
    """Load and filter data for the configured year."""
    filepath = os.path.join(EXPORT_DIR, WORK_FILE)
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
    else:
        log.error("Data file not found!")
        return None

    df[MODEL_DESCRIPTION] = (
    df[MODEL_DESCRIPTION]
        .str.strip()
        .str.upper()
    )

    df[MODEL_DATE] = pd.to_datetime(df[MODEL_DATE])
    df = df[df[MODEL_DATE].dt.year == YEAR]


    
    return df

def get_unknown_categories(df):
    """Return rows where category is missing or marked as unknown."""
    return df[
        df[MODEL_CATEGORY].isna() 
        | (df[MODEL_CATEGORY].str.strip() == "") 
        | (df[MODEL_CATEGORY].str.lower() == "unknown")
    ]

# -------------------------
# Financial Report Class
# -------------------------
class FinancialReport:
    def __init__(self, df):
        self.df = df
        self.expenses = get_expenses(df)
        self.income = get_income(df)
        self.metrics = {}

    def calculate_metrics(self):
        """Compute all summary metrics once and cache them."""
        total_income = self.income[MODEL_AMOUNT].sum()
        total_expense = self.expenses[MODEL_AMOUNT].sum()
        net_savings = total_income + total_expense  # expenses negative

        monthly_income_by_category = (
        self.income
            .groupby([self.income[MODEL_DATE].dt.month, MODEL_CATEGORY])[MODEL_AMOUNT]
            .sum()
        )

        monthly_income_by_description = (
            self.income
                .groupby([
                    self.income[MODEL_DATE].dt.month,
                    MODEL_DESCRIPTION
                ])[MODEL_AMOUNT]
                .sum()
        )

    
        monthly_expense = (
            self.expenses.groupby(self.df[MODEL_DATE].dt.month)[MODEL_AMOUNT].sum()
        )
        monthly_expense_by_category = (
            self.expenses.groupby([self.df[MODEL_DATE].dt.month, MODEL_CATEGORY])[
                MODEL_AMOUNT
            ].sum()
        )

        monthly_expense_by_description = (
            self.expenses
            .groupby([
                self.expenses[MODEL_DATE].dt.month,
                MODEL_DESCRIPTION
            ])[MODEL_AMOUNT]
            .sum()
        )


        # Largest/smallest spending months
        largest_spending_month = monthly_expense.idxmin()
        smallest_spending_month = monthly_expense.idxmax()

        # Biggest splurge
        biggest_splurge = self.expenses[MODEL_AMOUNT].min()

        # Most frequent vendor
        most_frequent_vendor = self.expenses[MODEL_DESCRIPTION].value_counts().idxmax()

        self.metrics = {
            "total_income": total_income,
            "total_expense": total_expense,
            "net_savings": net_savings,
            "monthly_income_by_category": monthly_income_by_category,
            "monthly_income_by_description": monthly_income_by_description,
            "monthly_expense": monthly_expense,
            "monthly_expense_by_category": monthly_expense_by_category,
            "monthly_expense_by_description": monthly_expense_by_description,  # 👈 NEW
            "largest_spending_month": calendar.month_name[largest_spending_month],
            "smallest_spending_month": calendar.month_name[smallest_spending_month],
            "biggest_splurge": biggest_splurge,
            "most_frequent_vendor": most_frequent_vendor,
        }

        return self.metrics

    def yearly_summary(self, file_name="yearly_summary.xlsx"):
        """Generate Excel summary of income, expenses, and totals."""
        filepath = os.path.join(EXPORT_DIR, file_name)

        expense_summary = (
            self.expenses.groupby(MODEL_CATEGORY)[MODEL_AMOUNT].sum().sort_values()
        )
        income_summary = (
            self.income.groupby(MODEL_CATEGORY)[MODEL_AMOUNT].sum().sort_values()
        )

        with pd.ExcelWriter(filepath) as writer:
            expense_summary.to_excel(writer, sheet_name="Expenses")
            income_summary.to_excel(writer, sheet_name="Income")

            summary_data = {
                "Metric": ["Total Expenses", "Total Income", "Net Savings"],
                "Amount": [
                    self.metrics["total_expense"],
                    self.metrics["total_income"],
                    self.metrics["net_savings"],
                ],
            }
            pd.DataFrame(summary_data).to_excel(
                writer, sheet_name="Summary", index=False
            )

        log.info(f"✅ Yearly summary saved to {filepath}")

    def save_monthly_income__by_category(self, file_name="monthly_income_by_category.xlsx"):
        """Pivot monthly expense by category and save to Excel."""
        filepath = os.path.join(EXPORT_DIR, file_name)
        pivot_df = self.metrics["monthly_income_by_category"].unstack().fillna(0).abs().T
        pivot_df.to_excel(filepath)
        log.info(f"✅ Monthly income by category saved to {filepath}")

    def save_monthly_expenses__by_category(self, file_name="monthly_expense_by_category.xlsx"):
        """Pivot monthly expense by category and save to Excel."""
        filepath = os.path.join(EXPORT_DIR, file_name)
        pivot_df = self.metrics["monthly_expense_by_category"].unstack().fillna(0).abs().T
        pivot_df.to_excel(filepath)
        log.info(f"✅ Monthly expense by category saved to {filepath}")

    
    def save_monthly_expenses_by_description(
    self, file_name="monthly_expense_by_description.xlsx"
):
        """Pivot monthly expenses by description and save to Excel."""
        filepath = os.path.join(EXPORT_DIR, file_name)

        pivot_df = (
            self.metrics["monthly_expense_by_description"]
                .unstack(fill_value=0)
                .abs()
                .T
        )

        pivot_df.to_excel(filepath)
        log.info(f"✅ Monthly expense by description saved to {filepath}")

    def save_monthly_income_by_description(
        self, file_name="monthly_income_by_description.xlsx"
    ):
        filepath = os.path.join(EXPORT_DIR, file_name)

        pivot_df = (
            self.metrics["monthly_income_by_description"]
                .unstack()
                .fillna(0)
                .T
        )

        pivot_df.to_excel(filepath)
        log.info(f"✅ Monthly income by description saved to {filepath}")

    def print_wrapup(self):
        """Log a quick financial wrap-up (like Spotify Wrapped)."""
        log.info("\n📊 Your Financial Wrapped")
        log.info(f"💸 Total Spent: ${-self.metrics['total_expense']:.2f}")
        log.info(f"💰 Total Income: ${self.metrics['total_income']:.2f}")
        log.info(f"📈 Net Savings: ${self.metrics['net_savings']:.2f}")
        log.info(f"📅 Largest Spending Month: {self.metrics['largest_spending_month']}")
        log.info(f"📅 Smallest Spending Month: {self.metrics['smallest_spending_month']}")
        log.info(f"🎯 Biggest Splurge: ${-self.metrics['biggest_splurge']:.2f}")
        log.info(f"☕ Most Frequent Vendor: {self.metrics['most_frequent_vendor']}")

    def get_unknowns(self, save=False, file_name="unknown_categories.csv"):
        """Print unknown categories and optionally save them to a file."""
        unknown_df = get_unknown_categories(self.df)

        # Print to console
        log.info("\n⚠️ Unknown Categories:")
        log.info(unknown_df)

        # Save if requested
        if save:
            filepath = os.path.join(EXPORT_DIR, file_name)
            unknown_df.to_csv(filepath, index=False)
            log.info(f"📁 Unknown categories saved to {filepath}")

        return unknown_df
