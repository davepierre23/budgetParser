import os
import pandas as pd
from config import DATA_DIR, WORK_FILE, MODEL_DATE, YEAR ,MODEL_DESCRIPTION, MODEL_AMOUNT, MODEL_SOURCE, MODEL_CLEAN_DESCRIPT
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
    tangerineCheque,
    Preferred__Package, 
    bmoParser
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
        tangerineCheque, 
        Preferred__Package,
        bmoParser
    ]


def process_files():
    """Parse, deduplicate, and return transaction data as a unified DataFrame."""
    if os.path.exists(WORK_FILE):
        # ✅ Load cached transactions
        df = pd.read_csv(WORK_FILE)
        df[MODEL_DATE] = pd.to_datetime(df[MODEL_DATE])
    else:
        parsers = load_parsers()
        parsed_data = []

        for filename in os.listdir(DATA_DIR):
            filepath = os.path.join(DATA_DIR, filename)

            # ✅ Skip unchanged files
            if not should_import(filepath):
                print(f"⏩ Skipping {filepath}, no new updates.")
                continue

            parsed = False
            for parser in parsers:
                if parser.canParse(filepath):
              
                    print(f"⚠️ Parser {parser.__name__}  data for {filepath}")
                    df_parsed = parser.parse(filepath)
                    

                    if df_parsed is None or df_parsed.empty:
                        print(f"⚠️ Parser {parser.__name__} returned no data for {filepath}")
                        continue
                    df_parsed[MODEL_SOURCE] = filename  # ✅ Track file origin

                    # ✅ Filter only new transactions
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

        df[MODEL_CLEAN_DESCRIPT] = df[MODEL_DESCRIPTION].apply(clean_pattern)


        # ✅ Deduplicate across all parsed files
        before_count = len(df)
        df = df.drop_duplicates(
            subset=[MODEL_DATE, MODEL_DESCRIPTION,MODEL_CLEAN_DESCRIPT,MODEL_AMOUNT, MODEL_SOURCE],
            keep="first"
        )
        after_count = len(df)
        print(f"🧹 Deduplication complete: removed {before_count - after_count} duplicate rows.")

    # ✅ Keep only rows from this year
    return df[df[MODEL_DATE].dt.year == YEAR]


def clean_pattern(text: str) -> str:
    """
    Cleans a transaction description so it becomes a stable keyword.
    Removes noise like:
    - numbers
    - store IDs (#1234)
    - city/province codes
    - extra spaces
    Keeps only keywords that are useful for categorization.
    """

    if not text or not isinstance(text, str):
        return ""

    t = text.upper()

    # Remove extra spaces
    t = t.replace("\n", " ").strip()

    # Remove punctuation
    import re
    t = re.sub(r"[^A-Z0-9\s]", " ", t)

    # Remove numbers (avoid store numbers like COSTCO #1244)
    t = re.sub(r"\d+", " ", t)

    # Remove province/city noise — OPTIONAL LIST, YOU CAN EXPAND
    remove_words = {
        "CANADA", "ONTARIO", "ONT", "ON", "QC", "QUEBEC", "OTTAWA", "VANCOUVER"
        "AB", "BC", "NS", "NB", "SK", "MB", "OPOS", "ORLEA", "ORLEANS", "SP",
        "CA", "USA", "US", "FPOS", "POS", "PURCHASE", "OTTAW" , "MONTR", "TORONTO"
    }

    parts = [p for p in t.split() if p not in remove_words]

    # If cleaning deletes everything → fall back to original
    if not parts:
        return text.upper().strip()

    # Join cleaned text
    cleaned = " ".join(parts)

    # Collapse multiple spaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned
