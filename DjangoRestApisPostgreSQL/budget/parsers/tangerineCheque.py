import sys
import logging
import pyexcel as p
from datetime import datetime
import sys
import pandas as pd
import logging as log
logging.basicConfig(format='%(message)s', level=logging.INFO)
from config import DATA_DIR, MODEL_DATE,  MODEL_AMOUNT,  MODEL_DESCRIPTION,  MODEL_ORIGIN
import os
import filecmp

directory =  "/Users/davepierre/Documents/Projects/budgetParser/data"

DATE='Date'
AMOUNT='Amount'
TANGERINE_SHEET='Money-Back Credit Card'
OUTPUT_DIRECTORY=''
DESCRIPTION = 'Name'

def canParse(full_path):
    return "4012914604.CSV"  in full_path or "Chequing.CSV" in full_path
def main(name):

    n = len(sys.argv)
    if(n>1):
        fileName = sys.argv[1]
    else:
        fileName = name

    summarize(parse(fileName), "month")
    summarize(parse(fileName), "year")
  
def containDuplicateFile(df):
    # Find the duplicated rows based on col1 and col2
    duplicated_rows = df.duplicated(subset=[DATE, 
    AMOUNT], keep=False)

    # Print only the duplicated rows
    if(df[duplicated_rows].empty):
        log.debug('No duplicate')
        return False
    else:
        log.debug('duplicates rows')
        return True
def parse(name):
    # load the Excel sheet into a pandas dataframe
    df =pd.read_csv(name, encoding='unicode_escape')
    df[DATE] = pd.to_datetime(df[DATE])
    df = convertToModels(df)
    return    parseEtransfer(df)

def parseEtransfer(df):
    etransfer_data = df[df[MODEL_DESCRIPTION].str.contains('INTERAC e-Transfer')].copy()

    if etransfer_data.empty:
        log.info("No INTERAC e-Transfers found in this dataset.")
        return

    etransfer_data.loc[:, MODEL_DATE] = pd.to_datetime(etransfer_data[MODEL_DATE])
    etransfer_data.loc[:, 'Year'] = etransfer_data[MODEL_DATE].dt.year
    etransfer_data.loc[:, 'Month'] = etransfer_data[MODEL_DATE].dt.month

    grouped_data = (
        etransfer_data
        .groupby(['Year', 'Month', MODEL_DESCRIPTION])[MODEL_AMOUNT]
        .sum()
        .reset_index()
    )

    log.info("E-Transfer Summary:")
    log.info("\n%s", grouped_data.to_string(index=False))  # prints nicely

def summarize(df, level="month"):
    if level == "year":
        grouped = df.groupby(df[MODEL_DATE].dt.year)[MODEL_AMOUNT].sum()
    elif level == "month":
        grouped = df.groupby([df[MODEL_DATE].dt.year, df[MODEL_DATE].dt.month])[MODEL_AMOUNT].sum()
    else:
        raise ValueError("Invalid level: choose 'year' or 'month'")

    log.info("Expense summary by %s:\n%s", level, grouped.to_string())
    return grouped


  
def convertToModels(df):
 
    new_df = df.loc[:, [DATE,DESCRIPTION, AMOUNT]]

    #basic model 
    #Date  #Description #Amount
    new_df.columns = [MODEL_DATE,MODEL_DESCRIPTION, MODEL_AMOUNT]
    new_df[MODEL_ORIGIN] = 'Tangerine'
    return new_df

if __name__ == "__main__":
    log.debug(parse(directory+"/4012914604.CSV"))
    

 