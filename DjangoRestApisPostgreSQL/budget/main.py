import pandas as pd
from config import WORK_FILE, EXPORT_DIR, MODEL_DESCRIPTION, MODEL_CATEGORY, categories
from processing import process_files
from categorizer import Categorizer
from parsers.ml_model import train_model, predict_unknowns
from reports import FinancialReport
import os
import shutil
import os
def clean_exports():
    if os.path.exists(EXPORT_DIR):
        shutil.rmtree(EXPORT_DIR)
    os.makedirs(EXPORT_DIR, exist_ok=True)

def main():
    clean_exports()
    os.makedirs(EXPORT_DIR, exist_ok=True)
    
    df = process_files()

    # Rule-based categorization
    cat = Categorizer(categories)
    df = cat.apply(df, MODEL_DESCRIPTION, MODEL_CATEGORY)

    # ML prediction
    model, vectorizer = train_model(df, MODEL_DESCRIPTION, MODEL_CATEGORY)
    if model:
        df = predict_unknowns(df, model, vectorizer, MODEL_DESCRIPTION, MODEL_CATEGORY)


    report = FinancialReport(df)
    report.calculate_metrics()
    report.yearly_summary()
    report.save_monthly_by_category()
    report.print_wrapup()

    # Save audit trail
    filepath = os.path.join(EXPORT_DIR, WORK_FILE)
    df.to_csv(filepath, index=False)
    print(f"✅ Exported processed data to: {filepath}")
    
if __name__ == "__main__":
    main()
