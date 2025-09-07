import sys
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
import logging
import pyexcel as p
from datetime import datetime
import sys
import pandas as pd
import logging as log
logging.basicConfig(format='%(message)s', level=logging.DEBUG)
from config import DATA_DIR, MODEL_DATE,  MODEL_AMOUNT,  MODEL_DESCRIPTION,  MODEL_ORIGIN

DATE='Pay Date'
AMOUNT='Net'
DATA_DIR = "/Users/davepierre/Documents/Projects/budgetParser/data/2022"

DESCRIPTION = 'Pay Type'


def main(name):

    n = len(sys.argv)
    if(n>1):
        fileName = sys.argv[1]
    else:
        fileName = name
    parse(name)
    

def parse(name):
     # load the Excel sheet into a pandas dataframe
    df = pd.read_excel(name, sheet_name='Paycheck history')

    df[DATE] = pd.to_datetime(df[DATE])
    #convert the values of the excel sheet 
    df[AMOUNT] = df[AMOUNT].str.replace('$', '').str.replace(',', '').astype(float)
    df = convertToModels(df)
    return df
def convertToModels(df):
   
    new_df = df.loc[:, [DATE,DESCRIPTION ,AMOUNT]]

    #basic model 
    #Date  #Description #Amount
    new_df.columns = [MODEL_DATE,MODEL_DESCRIPTION, MODEL_AMOUNT]
    new_df[MODEL_ORIGIN] = 'CBSAJOB'
    return new_df


def parseIncomeByMonth(name=""):
    df = parse(name)
    
   # group the data by month and year, and sum the income
    income_by_month_year = df.groupby([df[DATE].dt.year, df[DATE].dt.month])[AMOUNT].sum()

    # print the aggregated income by month and year
    log.debug(income_by_month_year)

def parseIncomeByYear(name=""):
    
    df = parse(name)
    
   # group the data by month and year, and sum the income
    income_by_year = df.groupby([df[DATE].dt.year])[AMOUNT].sum()

    # print the aggregated income by month and year
    log.debug(income_by_year)

def canParse(full_path):
    return "Paycheck history"  in full_path
  
if __name__ == "__main__":
    main(DATA_DIR+"/Paycheck history.xlsx")

