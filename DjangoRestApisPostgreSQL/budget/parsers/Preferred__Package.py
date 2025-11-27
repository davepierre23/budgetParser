import logging
import sys
import pandas as pd

import logging as log
logging.basicConfig(format='%(message)s', level=logging.INFO)
from config import DATA_DIR, MODEL_DATE,  MODEL_AMOUNT,  MODEL_DESCRIPTION,  MODEL_ORIGIN

DATE='Date'
AMOUNT='Amount'
DESCRIPTION='Sub-description' 
TYPE='Type'
NOTHING='NOTHING'
MONTHLY_FEE=' MONTHLY FEES'



ignores=['DILAWRI ' ,'EQUITABLE BANK' ,'American Express'
 'MB-CREDIT CARD/LOC PAY.' ,'Tangerine' ,'MB-TRANSFER'
 'ABM Withdrawal' ,'WITHDRAWAL', 'CANADA' ,'FREE INTERAC E-TRANSFER']



def canParse(full_path):
    return  "Preferred_Package"  in full_path and full_path.endswith('.csv')

def parse(name):
    """
    Parse a bank statement with columns:
    ['Filter', 'Date', 'Description', 'Sub-description',
     'Type of Transaction', 'Amount', 'Balance']
    """

    df =pd.read_csv(name, encoding='unicode_escape')



    # 1. Ensure required columns exist
    required = ["Date", "Description", "Sub-description", "Amount"]
    for col in required:
        if col not in df.columns:
            raise KeyError(f"Missing column: {col}")


    # 2. Merge Description + Sub-description
    df["FullDescription"] = (
        df["Description"].fillna("") + " " +
        df["Sub-description"].fillna("")
    ).str.strip()

    df = df.drop(columns=["Description"], errors="ignore")

    # 3. Convert date column
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # 4. Convert Amount to numeric
    df["Amount"] = (
        df["Amount"]
        .replace('[\$,]', '', regex=True)
        .astype(float)
    )

    # 5. Convert Balance to numeric if present
    if "Balance" in df.columns:
        df["Balance"] = (
            df["Balance"]
            .replace('[\$,]', '', regex=True)
            .astype(float)
        )

    # 6. Optional rule: make expenses negative
    # Example: Type of Transaction = "Debit" or "Withdrawal"
    if "Type of Transaction" in df.columns:
        df.loc[df["Type of Transaction"].str.contains("Debit|Withdrawal", case=False, na=False),
               "Amount"] *= -1

    # 7. Rename to standardized model
    df = df.rename(columns={
        "Date": MODEL_DATE,
        "FullDescription": MODEL_DESCRIPTION,
        "Amount": MODEL_AMOUNT
    })
    df =df[[MODEL_DATE, MODEL_DESCRIPTION, MODEL_AMOUNT]]
    df[MODEL_ORIGIN] = 'SCOTIA'
    log.info(f"Parsed {len(df)} rows from {df}")
    return df


def parseByMonth(name=""):
    df = parse(name)

    expense_by_month_year = df.groupby([df[DATE].dt.year, df[DATE].dt.month])[AMOUNT].sum()

    # print the aggregated income by month and year
    log.info(expense_by_month_year)

def parseMonthlyFeeByMonth(name=""):
    df = parse(name)
    # get rows where DESCRIPTION is "Monthly Fee"
    monthly_fees = df[df[MODEL_DESCRIPTION] == 'MONTHLY FEES']
    log.debug(monthly_fees)

    # print the resulting DataFrame
    monthly_fees = monthly_fees.groupby([monthly_fees[DATE].dt.year, monthly_fees[DATE].dt.month])[AMOUNT].sum()

    # print the aggregated income by month and year
    log.debug(monthly_fees)

def parseMonthlyFeeByYear(name=""):
    df = parse(name)
    # get rows where DESCRIPTION is "Monthly Fee"
    monthly_fees = df[df[MODEL_DESCRIPTION] == 'MONTHLY FEES']
    log.debug(monthly_fees)

    # print the resulting DataFrame
    monthly_fees = monthly_fees.groupby([monthly_fees[DATE].dt.year])[AMOUNT].sum()

    # print the aggregated income by month and year
    log.debug(monthly_fees)

def parseByYear(name=""):
    
    df = parse(df)

   # group the data by month and year, and sum the income
    expense_by_year = df.groupby([df[DATE].dt.year])[AMOUNT].sum()

    # print the aggregated income by month and year
    log.debug(expense_by_year)
    
def removeIgnored(df):


    # Use the `isin` method to check if the "DESCRIPTION" is in the `ignores` list
    mask = ~df[MODEL_DESCRIPTION].isin(ignores)

    # Apply the mask to filter out rows that are not in the `ignores` list
    return df[mask]

def convertToModels(df):
 
    new_df = df.loc[:, [DATE,DESCRIPTION, AMOUNT]]
    new_df[MODEL_DESCRIPTION]= new_df[MODEL_DESCRIPTION].str.strip()
    new_df = removeIgnored(new_df)

    #basic model 
    #Date  #Description #Amount
    new_df.columns = [MODEL_DATE,MODEL_DESCRIPTION, MODEL_AMOUNT]
    new_df[MODEL_ORIGIN] = 'SCOTIA'
 
    log.info(new_df)
    return new_df
def main(name):

    n = len(sys.argv)
    if(n>1):
        filename = sys.argv[1]
    else:
        filename = name
    parseMonthlyFeeByYear(filename)


if __name__ == "__main__":
    main(DATA_DIR+"Preferred_Package_9485_112625.csv")
    