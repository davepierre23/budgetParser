import scotiaParser
import americianExpressParser
import CBSAPayHistory
import tangerineParser
import pandas as pd
import sys
import os

import logging as log
log.basicConfig(format='%(message)s', level=log.INFO)
DATA_DIR = "/Users/davepierre/Documents/Projects/budgetParser/data"
WORK_FILE='my_data.csv'
MODEL_DATE='Date'
MODEL_DESCRIPTION= 'Description'
MODEL_AMOUNT= 'Amount'
MODEL_ORIGIN= 'Origin'
MODEL_CATEGORY= 'Category'


    # Define categories based on keywords in the "Description" column
categories = {
        "Alcohol": ["LCBO/RAO"],
        "Food": [  "JACK ASTOR'S","MCDONALD'S","Seoul Dog","REXALL","PIZZERIA","COBS BREAD","MILKMAN ","SUSHI","BRIG","LEXINGTON SMOKEHOUSE",'CHICK-FIL-A' ,"KFC","FRUIT","BROADWAY","DELICIOUS STEAKHOUSE","TIM HORTONS","STARBUCKS", "LUNCHBOX","Wild Wing ", "THE ALLEY","GYUBEE","RED LOBSTER", 'MENCHIE',"SQ *PANCHO'S ", "DAOL" , "SOUL STONE","MR. PRETZEL","METROPOLITAIN",
                    "St. Louis Bar","Bagel","LE ST LAURENT","MAVERICK'S",'POPEYES', "Chatime ","SOBEYS",'SHAKER',"MARY BROWN'S","SUSHI KAN","MANDARIN", "SHOPPERS",
            "WENDY'S", 'LE MIEN',"METRO","JOLLIBEE-","MOXIES","T&T","LOBLAWS","AZTEC","GREEN FRESH","FARM BOY","TEALIVE","BOSTON PIZZA","EAST SIDE MARIO",
            "Pizza Pizza ",'THE GREAT CANADIAN PO', 'UBER EATS ', "Shoppers Drug Mart",'BIG BONE BBQ',"NSEYA'S"],
        "Wardrobe": ["Tip Top", "Shoe Company",'SP JOJIKA','SHEIN',"VALUE VILLAGE","OVO"],
        "Entertainment": [
            "NORDIK",
            "TEE 2 GREEN",
            "DOLLYS",
            "STEAM",
            "TICKET",
            "LANDMARK",
            "WHITE SANDS",
            "Orleans Bowling.com",
            "BOWLING",
            "Top Karting Hull",
            "Sunrise Records",
            "SP TSX1",
            'eBay',
            'GAMESTOP',
            "CARTA",
            'Canada Computers',
            'PLAYSTATION',
            'RED DRAGON',
            'TCGPLAYER.COM',
            "401 GAMES"
  
        ],
        'Transporation':[ "Uber ","Lyft",'PRESTO',"PPARK","BUSBUD"],
        "Doctors/dental/vision":["APPLE'S CROWN",'ACE OF SPADES',"CLEARVIEW"],
        "Beauty":["CLORE","MONTEGO","MONAT"],
        "Gym":   [ "SHOWCASE ","SP CROSSROPE",'FIT4LESS'],
        "Home goods": ["AMZN", "APPLE","Dollarama","PANDABUY","BEST BUY","DOLLAR TREE","GIANT TIGER","CDN TIRE","HUDSON'S BAY",'AMAZON','WAL-MART'],
        'Income':['Basic Pay','Acting / Appointment Pay'],
        'Gas':['PIONEER',"ULTRAMAR",'CIRCLEK',"MOBIL","GAS","PETROCAN", 'MRGAS','ESSO','SHELL',"FUEL"],
        'Church':["CALVARY CHURCH"],
        'Education':["OPTIONS"],
        "Miscellaneous Payement": [
            "Dishonoured Payment",
            "Returned Payment",
            'REFUNDED'
        ],
        "Miscellaneous Charges": [
            'MONTHLY FEES',
            "Dishonoured Payment",
            "PREMIUM"
         
        ]
    }
def loadList():
    parsers =[]
    parsers.append(scotiaParser)
    parsers.append(americianExpressParser)
    parsers.append(CBSAPayHistory)
    parsers.append(tangerineParser)
    return parsers


def parse():


    if os.path.exists(WORK_FILE):
        df = pd.read_csv(WORK_FILE)
    else:
    
        parsedData=[]
        parsers= loadList()

        # Loop through each file in the directory
        for filename in os.listdir(DATA_DIR):
            filepath = os.path.join(DATA_DIR, filename)
            print(filepath)


            for  parse  in parsers:
                if(parse.canParse(filepath)):
                    parsedData.append(parse.parse(filepath))
        df = parsedData[0]  
       
        for data  in range(len(parsedData) ):
            if(data ==1):
                df = parsedData[0]          
            else:
                df = pd.concat([df, parsedData[data]], axis=0)
        df[MODEL_DATE] = pd.to_datetime(df[MODEL_DATE] ) 
        addCategorize(df)
        df.to_csv(WORK_FILE, index=False)

    df[MODEL_DATE] = pd.to_datetime(df[MODEL_DATE] ) 
    parseExpenseCatogeryByMonth(df)
    parseExpenseCategoryByYear(df)

   


def printUniqueNames(df):

    print(df[MODEL_DESCRIPTION].unique())


def addCategorize(df):
       # Add a new column to the dataframe based on categories
    df[MODEL_CATEGORY] = df.apply(categorize, axis=1)

def printResults(df):
    # Iterate over each row and print it
    for i in range(0, len(df), 5):
        print(df.iloc[i:i+5])
        print()  # add a blank line between groups of 5 rows

# Function to determine the category of a given row in the dataframe
def categorize(row):
    for category, keywords in categories.items():
        for keyword in keywords:
            if isinstance(row[MODEL_DESCRIPTION], float):
                print("float", row[MODEL_DESCRIPTION])
            else:
                if(row[MODEL_DESCRIPTION].upper().strip().find(keyword.upper().strip())>-1):
                    return category

                
    print(row[MODEL_DESCRIPTION])
    return 'Unknown'

def parseExpenseByMonth(df):
    expense = df[df[MODEL_AMOUNT] < 0]
    expense_by_month_year = expense.groupby([expense[MODEL_DATE].dt.year, expense[MODEL_DATE].dt.month,MODEL_CATEGORY])[MODEL_AMOUNT].sum()

    # print the aggregated income by month and year
    log.info(expense_by_month_year)

def parseExpenseCatogeryByMonth(df):
    expense = df[df[MODEL_AMOUNT] < 0]


    # Group the data by month, year, and category, and sum the 'Amount' column
    expense_by_month_year = expense.groupby([MODEL_CATEGORY,expense[MODEL_DATE].dt.year,expense[MODEL_DATE].dt.month])[MODEL_AMOUNT].sum()

    # print the aggregated income by month and year
    printResults(expense_by_month_year)

def parseExpenseCategoryByYear(df):

   # group the data by month and year, and sum the income
    expense = df[df[MODEL_AMOUNT] < 0]
     # Group the data by month, year, and category, and sum the 'Amount' column
    expense_by_year = expense.groupby([MODEL_CATEGORY,expense[MODEL_DATE].dt.year])[MODEL_AMOUNT].sum()

    # print the aggregated income by month and year
    log.info(expense_by_year)


def parseExpenseByYear(df):

   # group the data by month and year, and sum the income
    expense = df[df[MODEL_AMOUNT] < 0]
    expense_by_year = expense.groupby([expense[MODEL_DATE].dt.year])[MODEL_AMOUNT].sum()

    # print the aggregated income by month and year
    log.info(expense_by_year)


if __name__ == "__main__":
    parse()