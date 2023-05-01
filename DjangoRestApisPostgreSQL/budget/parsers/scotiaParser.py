import logging
import sys
import pandas as pd

import logging as log
logging.basicConfig(format='%(message)s', level=logging.DEBUG)
DATA_DIR = "/Users/davepierre/Documents/Projects/budgetParser/data/"
DATE='Date'
AMOUNT='Amount'
DESCRIPTION='Description'
TYPE='Type'
NOTHING='NOTHING'
MONTHLY_FEE=' MONTHLY FEES'

MODEL_DATE='Date'
MODEL_DESCRIPTION= 'Description'
MODEL_AMOUNT= 'Amount'
MODEL_ORIGIN= 'Origin'
def canParse(full_path):
    return  "pcbanking"  in full_path 

def parse(name):
    df = pd.read_csv(name)
    if(df.shape[1]==3):
        df.columns = [DATE,DESCRIPTION, AMOUNT]
    elif(df.shape[1]==5):
        df.columns = [DATE, AMOUNT,NOTHING,TYPE, DESCRIPTION]
        # drop the 'Nothing' column
        df = df.drop(NOTHING, axis=1)

    df[DATE] = pd.to_datetime(df[DATE])
    df = df[df[AMOUNT] < 0]
    return convertToModels(df)


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

def convertToModels(df):
 
    new_df = df.loc[:, [DATE,DESCRIPTION, AMOUNT]]

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
    main(DATA_DIR+"pcbanking 2.csv")
    