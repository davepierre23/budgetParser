import os
import shutil
import pandas as pd

from config import WORK_FILE, EXPORT_DIR, CATEGORY_FILE,MODEL_DESCRIPTION, MODEL_CATEGORY, MODEL_AMOUNT, MODEL_CLEAN_DESCRIPT
from categories import categories   # ✅ keep categories in categories.py
from processing import process_files
from categorizer import Categorizer
from parsers.ml_model import train_model, predict_unknowns
from reports import FinancialReport
from state_manager import update_last_run


def clean_exports():
    """Clear old exports and recreate the directory."""
    if os.path.exists(EXPORT_DIR):
        archive_dir = os.path.join(EXPORT_DIR, "archive")
        os.makedirs(archive_dir, exist_ok=True)

        # Move old files instead of deleting
        for f in os.listdir(EXPORT_DIR):
            full_path = os.path.join(EXPORT_DIR, f)
            if os.path.isfile(full_path):
                shutil.move(full_path, os.path.join(archive_dir, f))

    os.makedirs(EXPORT_DIR, exist_ok=True)


def main():
    clean_exports()
    
    # Process input transaction files
    df = process_files()

    # Rule-based categorization
    cat = Categorizer(categories, CATEGORY_FILE)
    df = cat.apply(df, MODEL_CLEAN_DESCRIPT, MODEL_CATEGORY)
    df = cat.interactive_categorizer(df)

    # ML-based categorization for unknowns
    model, vectorizer = train_model(df, MODEL_CLEAN_DESCRIPT, MODEL_CATEGORY)
    # if model:
    #     df = predict_unknowns(df, model, vectorizer, MODEL_DESCRIPTION, MODEL_CATEGORY)

    # Gift card deal checker
    deal_checker = GiftCardDealChecker()
    results = deal_checker.scan(df, description_col=MODEL_CLEAN_DESCRIPT, amount_col=MODEL_AMOUNT)
    deal_checker.print_results(results)

    # Generate reports
    report = FinancialReport(df)
    report.calculate_metrics()
    report.yearly_summary()
    report.save_monthly_expenses__by_category()
    report.save_monthly_income__by_category()
    report.print_wrapup()
    report.get_unknowns(True)

    # Save audit trail
    output_file = os.path.join(EXPORT_DIR, WORK_FILE)
    df.to_csv(output_file, index=False)
    print(f"✅ Exported processed data to: {output_file}")

    # Update state after successful run
    update_last_run()


if __name__ == "__main__":
    main()
