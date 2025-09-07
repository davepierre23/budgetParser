import sys
import logging
import pyexcel as p
from datetime import datetime
import sys
import pandas as pd
import logging as log
logging.basicConfig(format='%(message)s', level=logging.INFO)
import os
import filecmp

directory =  "/Users/davepierre/Documents/Projects/budgetParser/data"

DATE='Date'
AMOUNT=' Funds Out'
TANGERINE_SHEET='Money-Back Credit Card'
OUTPUT_DIRECTORY=''
COMBINED_SHEET= 'combined_Tangerine.csv'
DESCRIPTION = ' Transaction Details'

MODEL_DATE='Date'
MODEL_DESCRIPTION= 'Description'
	 	 
MODEL_AMOUNT= 'Amount'
MODEL_ORIGIN= 'Origin'
def combineTangerineSheets():
    removeDuplicateFiles()

    # Initialize an empty DataFrame to hold the combined data
    combined_data = pd.DataFrame()

    # Loop through each file in the directory
    for filename in os.listdir(directory):
        if filename.startswith(TANGERINE_SHEET):  # check if the file is an Excel file
            log.debug(filename)
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)
            combined_data = combined_data.append(df, ignore_index=True)

    # Write the combined data to a new Excel file
    combined_data.to_csv(OUTPUT_DIRECTORY+COMBINED_SHEET, index=False)
def canParse(full_path):
    return "SIMPLII.csv"  in full_path
def main(name):

    n = len(sys.argv)
    if(n>1):
        fileName = sys.argv[1]
    else:
        fileName = name
    parseByYear(fileName)
    parseByMonth(fileName)
  
def removeDuplicateFiles():
    # Get a list of CSV files in the directory
    csv_files = [f for f in os.listdir(directory) if f.startswith(TANGERINE_SHEET)]

    # Check for duplicate files and delete them
    for i, file1 in enumerate(csv_files):
        for file2 in csv_files[i+1:]:
            if filecmp.cmp(os.path.join(directory, file1), os.path.join(directory, file2)):
                os.remove(os.path.join(directory, file2))

def containDuplicateFile(df):
    # Find the duplicated rows based on col1 and col2
    duplicated_rows = df.duplicated(subset=[DATE, 
    AMOUNT], keep=False)

    # Print only the duplicated rows
    if(df[duplicated_rows].empty):
        print('No duplicate')
        return False
    else:
        print('duplicates rows')
        return True
def parse(name):
    # load the Excel sheet into a pandas dataframe
    df =pd.read_csv(name, encoding='unicode_escape')
    df[DATE] = pd.to_datetime(df[DATE])
    # #convert the values of the excel sheet 
    # df[AMOUNT] = df[AMOUNT].astype(float)
    # df = df[df[AMOUNT] < 0]
    df = convertToModels(df)
    parseEtransfer(df)

    return df

def parseEtransfer(df):

    # Filter rows where the 'Name' column contains 'INTERAC e-Transfer'
    etransfer_data = df[df[MODEL_DESCRIPTION].str.contains('INTERAC e-Transfer')]
 
    # Convert 'Date' column to datetime if it's not already in datetime format
    etransfer_data[MODEL_DATE] = pd.to_datetime(etransfer_data[MODEL_DATE])

    # Extract the year from the 'Date' column
    etransfer_data['Year'] = etransfer_data[MODEL_DATE].dt.year
    etransfer_data['Month'] = etransfer_data[MODEL_DATE].dt.month

    # Group by 'Year' and 'Description', then calculate the sum of 'Amount' for each group
    # Group by 'Year', 'Month', and 'Description', then calculate the sum of 'Amount' for each group
    grouped_data = etransfer_data.groupby(['Year', 'Month', MODEL_DESCRIPTION])[MODEL_AMOUNT].sum().reset_index()

    # Print the grouped data
    print(grouped_data)
 
def parseByMonth(name=""):

    df = parse(name)

   # group the data by month and year, and sum the income
    expense_by_month_year = df.groupby([df[MODEL_DATE].dt.year, df[MODEL_DATE].dt.month])[MODEL_AMOUNT].sum()

    # print the aggregated income by month and year
    log.info(expense_by_month_year)

def parseByYear(name=""):

    df = parse(name)

   # group the data by month and year, and sum the income
    expense_by_year = df.groupby([df[MODEL_DATE].dt.year])[MODEL_AMOUNT].sum()

    # print the aggregated income by month and year
    log.info(expense_by_year)
    return 
  
def convertToModels(df):

    # Check the column names of the DataFrame
    print("Columns in DataFrame:", df.columns)

    # Ensure required columns exist
    required_columns = [DATE, DESCRIPTION, AMOUNT]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"Missing required column: {col}")

    # Extract required columns
    new_df = df.loc[:, [DATE, DESCRIPTION, AMOUNT]]
    print(new_df)

    # Rename columns to model names
    new_df.columns = [MODEL_DATE, MODEL_DESCRIPTION, MODEL_AMOUNT]

    # Add an origin column
    new_df[MODEL_ORIGIN] = 'SIMPLI'

    # Remove rows where the 'Amount' column has NaN
    cleaned_df = new_df.dropna(subset=[MODEL_AMOUNT])
    


    return cleaned_df

if __name__ == "__main__":
    print(parse(directory+"/SIMPLII.csv"))
    

  