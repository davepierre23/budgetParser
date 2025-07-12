import pandas as pd
from datetime import datetime

directory =  "/Users/davepierre/Downloads"

MODEL_DATE = 'Date'
MODEL_DESCRIPTION = 'Description'
MODEL_AMOUNT = 'Amount'
MODEL_ORIGIN = 'Origin'


def canParse(filepath):
    try:
        df = pd.read_csv(filepath, nrows=1)
        return 'ID' in df.columns and 'Direction' in df.columns and 'Source amount (after fees)' in df.columns
    except:
        return False


def parse(filepath):
    df = pd.read_csv(filepath)

    # Filter only completed, outgoing transactions
    df = df[(df['Status'] == 'COMPLETED') & (df['Direction'] == 'OUT')]

    # Parse dates
    df[MODEL_DATE] = pd.to_datetime(df['Created on'])

    # Description = Target name
    df[MODEL_DESCRIPTION] = df['Target name']

    # Set exchange rate from JPY to CAD (you can make this dynamic later)
    JPY_TO_CAD = 0.0091

    # Handle amount conversion
    def convert_amount(row):
        amount = -row['Source amount (after fees)']
        if row['Source currency'] == 'JPY':
            return amount * JPY_TO_CAD
        return amount

    df[MODEL_AMOUNT] = df.apply(convert_amount, axis=1)

    # Origin
    df[MODEL_ORIGIN] = 'Wise'

    return df[[MODEL_DATE, MODEL_DESCRIPTION, MODEL_AMOUNT, MODEL_ORIGIN]]


if __name__ == "__main__":
    print(parse(directory+"/transaction-history.csv"))
    

  