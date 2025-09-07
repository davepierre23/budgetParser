import pandas as pd
from config import WORK_FILE, MODEL_DESCRIPTION, MODEL_CATEGORY, categories
from processing import process_files
from categorizer import Categorizer
from parsers.ml_model import train_model, predict_unknowns
from reports import FinancialReport

def main():
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
    df.to_csv(WORK_FILE, index=False)

if __name__ == "__main__":
    main()
