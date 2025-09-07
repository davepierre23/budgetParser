import os, pandas as pd
from config import DATA_DIR, WORK_FILE, MODEL_DATE, YEAR
from categorizer import Categorizer
from parsers.ml_model import train_model, predict_unknowns
from parsers import scotiaParser, americianExpressParser, simpliCreditParser, CBSAPayHistory, tangerineParser, wealthSimple, wiseParser

def load_parsers():
    return [scotiaParser, americianExpressParser, simpliCreditParser, CBSAPayHistory, tangerineParser, wealthSimple, wiseParser]

def process_files():
    """Parse and process transaction files into a unified DataFrame."""
    if os.path.exists(WORK_FILE):
        df = pd.read_csv(WORK_FILE)
    else:
        parsers = load_parsers()
        parsed_data = []

        for filename in os.listdir(DATA_DIR):
            filepath = os.path.join(DATA_DIR, filename)
            parsed = False

            for parser in parsers:
                if parser.canParse(filepath):
                    parsed_data.append(parser.parse(filepath))
                    parsed = True
                    break

            if not parsed:
                print(f"⚠️ Could not parse: {filepath}")

        if not parsed_data:
            raise ValueError("No valid data was parsed.")

        df = pd.concat(parsed_data, ignore_index=True)
        df[MODEL_DATE] = pd.to_datetime(df[MODEL_DATE])
        df.to_csv(WORK_FILE, index=False)

    df[MODEL_DATE] = pd.to_datetime(df[MODEL_DATE])
    return df[df[MODEL_DATE].dt.year == YEAR]
