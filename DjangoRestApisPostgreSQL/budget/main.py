import pandas as pd
from config import WORK_FILE, MODEL_DESCRIPTION, MODEL_CATEGORY
from processing import process_files
from categorizer import Categorizer
from parsers.ml_model import train_model, predict_unknowns
#from reports import calculate_metrics, print_wrapup, save_monthly_expense_by_category
from categories import categories

def main():
    df = process_files()

    # Rule-based categorization
    cat = Categorizer(categories)
    df = cat.apply(df, MODEL_DESCRIPTION, MODEL_CATEGORY)

    # ML prediction
    model, vectorizer = train_model(df, MODEL_DESCRIPTION, MODEL_CATEGORY)
    if model:
        df = predict_unknowns(df, model, vectorizer, MODEL_DESCRIPTION, MODEL_CATEGORY)

    # Reporting
    # metrics = calculate_metrics(df)
    # print_wrapup(metrics)
    # save_monthly_expense_by_category(metrics)

    # Save audit trail
    df.to_csv(WORK_FILE, index=False)

if __name__ == "__main__":
    main()
