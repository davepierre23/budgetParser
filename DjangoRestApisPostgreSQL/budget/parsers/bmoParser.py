import logging
import sys
import pandas as pd

import logging as log
logging.basicConfig(format='%(message)s', level=logging.INFO)

from config import (
    DATA_DIR,
    MODEL_DATE,
    MODEL_AMOUNT,
    MODEL_DESCRIPTION,
    MODEL_ORIGIN
)

# Raw columns
CARD = "First Bank Card"
TX_DATE = "Date Posted"
POST_DATE = "Posting Date"
AMOUNT = " Transaction Amount"
DESCRIPTION = "Description"

IGNORES = [
    # optional: uncomment if you want to exclude payments
    # "PAYMENT RECEIVED - THANK YOU",
]

def canParse(full_path: str) -> bool:
    return full_path.endswith(".csv") and "statement" in full_path


def parse(name: str) -> pd.DataFrame:
    """
    Parses credit card transaction export with leading metadata row.
    """

    # 1. Skip metadata row, header is row 1
    df = pd.read_csv(
        name,
        skiprows=3,
        encoding="unicode_escape"
    )

    df = df.apply(lambda c: c.str.strip() if c.dtype == "object" else c)


    # 4. Convert YYYYMMDD → datetime
    df[TX_DATE] = pd.to_datetime(df[TX_DATE], format="%Y%m%d", errors="coerce")


    # 6. Optional ignore filter
    if IGNORES:
        df = df[~df[DESCRIPTION].isin(IGNORES)]

    # 7. Rename to standardized model
    df = df.rename(columns={
        TX_DATE: MODEL_DATE,
        DESCRIPTION: MODEL_DESCRIPTION,
        AMOUNT: MODEL_AMOUNT
    })

    df = df[[MODEL_DATE, MODEL_DESCRIPTION, MODEL_AMOUNT]]
    df[MODEL_ORIGIN] = "CREDIT_CARD"

    log.info(f"Parsed {len(df)} rows from {name}")
    return df


# --------------------------
# AGGREGATIONS
# --------------------------

def parseByMonth(name: str):
    df = parse(name)
    result = df.groupby(
        [df[MODEL_DATE].dt.year, df[MODEL_DATE].dt.month]
    )[MODEL_AMOUNT].sum()
    log.info(result)


def parseByYear(name: str):
    df = parse(name)
    result = df.groupby(
        df[MODEL_DATE].dt.year
    )[MODEL_AMOUNT].sum()
    log.info(result)


def parseInterestOnly(name: str):
    df = parse(name)
    interest = df[df[MODEL_DESCRIPTION].str.contains("INTEREST", case=False)]
    log.info(interest)


def main(name=""):
    filename = sys.argv[1] if len(sys.argv) > 1 else name
    parseByYear(filename)


if __name__ == "__main__":
    main(DATA_DIR + "Card_Transactions.csv")
