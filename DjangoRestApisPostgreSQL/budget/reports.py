import pandas as pd
from collections import defaultdict
import logging

log = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self, transactions: pd.DataFrame):
        """
        transactions: DataFrame with columns [Date, Description, Amount, Category, Origin, Method]
        """
        self.transactions = transactions

    def summary_by_category(self):
        """Return total spent per category"""
        summary = (
            self.transactions.groupby("Category")["Amount"]
            .sum()
            .sort_values(ascending=False)
        )
        log.info("Generated category summary")
        return summary

    def monthly_spending(self):
        """Return spending by month"""
        df = self.transactions.copy()
        df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")
        summary = (
            df.groupby("Month")["Amount"]
            .sum()
            .sort_index()
        )
        log.info("Generated monthly spending report")
        return summary

    def top_merchants(self, n=5):
        """Return top merchants by spending"""
        summary = (
            self.transactions.groupby("Description")["Amount"]
            .sum()
            .sort_values(ascending=False)
            .head(n)
        )
        log.info(f"Generated top {n} merchants report")
        return summary

    def export_csv(self, filepath="reports/summary.csv"):
        """Export the full transactions with categories to CSV"""
        self.transactions.to_csv(filepath, index=False)
        log.info(f"Exported report to {filepath}")
        return filepath
