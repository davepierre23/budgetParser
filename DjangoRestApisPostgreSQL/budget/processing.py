import os
import pandas as pd
from config import DATA_DIR, WORK_FILE, MODEL_DATE, YEAR
from categorizer import Categorizer
from parsers.ml_model import train_model, predict_unknowns
from parsers import (
    scotiaParser,
    americianExpressParser,
    simpliCreditParser,
    CBSAPayHistory,
    tangerineParser,
    wealthSimple,
    wiseParser,
)
from state_manager import update_last_download, should_import, get_new_transactions


def load_parsers():
    return [
        scotiaParser,
        americianExpressParser,
        simpliCreditParser,
        CBSAPayHistory,
        tangerineParser,
        wealthSimple,
        wiseParser,
    ]


def process_files():
    """Parse and process transaction files into a unified DataFrame."""
    if os.path.exists(WORK_FILE):
        # Load cached transactions
        df = pd.read_csv(WORK_FILE)
        df[MODEL_DATE] = pd.to_datetime(df[MODEL_DATE])
    else:
        parsers = load_parsers()
        parsed_data = []

        for filename in os.listdir(DATA_DIR):
            filepath = os.path.join(DATA_DIR, filename)

            # Skip if file hasn’t changed since last import
            if not should_import(filepath):
                print(f"⏩ Skipping {filepath}, no new updates.")
                continue

            parsed = False
            for parser in parsers:
                if parser.canParse(filepath):
                    df_parsed = parser.parse(filepath)

                    # ✅ Keep only rows newer than last run
                    df_new = get_new_transactions(df_parsed, MODEL_DATE)

                    if not df_new.empty:
                        parsed_data.append(df_new)
                        update_last_download(filepath)
                        print(f"✅ Parsed {len(df_new)} new rows from {filepath}")
                    else:
                        print(f"ℹ️ No new transactions in {filepath}")

                    parsed = True
                    break

            if not parsed:
                print(f"⚠️ Could not parse: {filepath}")

        if not parsed_data:
            raise ValueError("No valid data was parsed.")

        df = pd.concat(parsed_data, ignore_index=True)
        df[MODEL_DATE] = pd.to_datetime(df[MODEL_DATE])

    # Keep only this year's data
    return df[df[MODEL_DATE].dt.year == YEAR]
