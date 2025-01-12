import scotiaParser
import americianExpressParser 
import simpliCreditParser
import CBSAPayHistory
import tangerineParser
import wealthSimple
import pandas as pd
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
YEAR =2024
    # Define categories based on keywords in the "Description" column


categories = {
        "Wealthsimple":["Wealthsimple"],
        "Alcohol": ["LCBO/RAO","PURE BREW"],
        "Groceries":["TooGoodT ",'FLASHFOOD','HALIBUT HOUSE ','WALMART.CA','FRESHCO',"BULK BARN","DUNKIN", "REVOLUTIONN","NO FRILLS", 'FOOD BASICS',"METRO","SOBEYS","LOBLAWS","WAL*MART","NSEYA'S","Shoppers Drug Mart","FARM BOY","REXALL",],
        "Restaurents": [ "MIKE DEAN'S","Cafe","LITTLE CAESARS","ROYAL OAK","BOOSTER JUICE ",'CORA',"HALIBUT",'TIPIKLIZ','HARVEY','LEVEL ONE',"DAIRY QUEEN","SHOELESS JOES", "Subway","FOOD",'PITA BELL KABAB', "Chances",'SHAWARMA PALACE', 'WENDYS', 'LOUIS', "JONNY CANUCK'S", 'CAFÉ LATTE', 'NOM NOM', 'PRESOTEA', 'HEY KITCHEN', 'MEZZANOTTE', 'A&W',"BAKERY","DOUGHNUTS","JACK ASTOR'S","MCDONALD'S","DOORDASH","Seoul Dog","PIZZERIA",'FAIRMONT CHATEAU LAURIE ',"COBS BREAD","MILKMAN ","SUSHI","BRIG","LEXINGTON SMOKEHOUSE",'CHICK-FIL-A' ,"KFC","FRUIT","BROADWAY","DELICIOUS STEAKHOUSE","TIM HORTONS","STARBUCKS", "LUNCHBOX","Wild Wing ", "THE ALLEY","GYUBEE","RED LOBSTER", 'MENCHIE',"SQ *PANCHO'S ", "DAOL" , "SOUL STONE","MR. PRETZEL","METROPOLITAIN",
                    "St. Louis Bar","Bagel","COCO FRESH TEA ","LE ST LAURENT","MAVERICK'S",'POPEYES', "Chatime ",'SHAKER',"MARY BROWN'S","SUSHI KAN","MANDARIN", "SHOPPERS",
             "WENDY'S", 'LE MIEN',"JOLLIBEE-","MOXIES","T&T","AZTEC","GREEN FRESH","TEALIVE","BOSTON PIZZA","EAST SIDE MARIO",
            "Pizza Pizza ",'THE GREAT CANADIAN PO','Carleton Web', 'UBER EATS ', 'BIG BONE BBQ',],
        "Clothing": ["Tip Top","SPORT CHEK",'WINNERS','ADIDAS','SPORTS', 'OLD NAVY',"THE GAP","FAIRWEATHER","THREADS TAILORS","Shoe Company",'SP JOJIKA','SHEIN',"VALUE VILLAGE","OVO","BOATHOUSE","LEZE THE LABEL"],

        "Entertainment": [
            "DOOLY'S OTTAWA INC. OTTAWA ON",
            "DISNEYPLUS",
            "GOLF",
            "FALCON RIDGE",
            "PUTTING EDGE",
            "NORDIK",
            "TEE 2 GREEN",
            "DOLLYS",
            "STEAM",
            "PHD IN WAVES",
            "CALYPSO",
            "TICKET",
            "SMASH ROOM",
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
            "VRADVENTURES.ZONE ",
            'VR ADVENTURES.ZONE',
            "EVENTBRITE",
            "TCGPLAYER ",
            'TCGPLAYER.COM',
            "401 GAMES",
         "Wtbmatters"
  
        ],
        "Car Loan":["Loan Payment","BANK STREET MAZDA"],
        "Car Maintenance":["OIL CHANGERS","Caps Auto","CARLING TIRE "],
        "Travel":["Airlines ","FLIGHTHUB","AIRBNB",'AIRCANADA'],

        "Car Insurance":["BELAIR INS/ASS","BELAIRDIRECT"],
        "Online Shopping":["LEGO","JEWELLERS","HIVEMAPPER","MY USADDRESS","AFROBLAST","SIMPLYMODBOX"],
        'Transporation':[ "Uber ","Lyft",'PRESTO',"PPARK","BUSBUD"],
        "Doctors/dental/vision":["APPLE'S CROWN",'ACE OF SPADES',"CLEARVIEW","KITS","Echo","LASIK MD","PHYSIO"],
        "Personal Care":["CLORE","MONTEGO","MONAT","NANCY'S NAILS AND LASHE","BATH & BODY WORKS"],
        "Gym":   [ "SHOWCASE ","SP CROSSROPE",'FIT4LESS', "OTTAWACITY"],
        "Home goods": ["AMZN", "APPLE","QUICK PICK","Dollarama","PANDABUY","BEST BUY","DOLLAR TREE","GIANT TIGER","CDN TIRE","HUDSON'S BAY",'AMAZON','WAL-MART'],
        'Income':['Basic Pay','Acting / Appointment Pay'],
        'Gas':['PIONEER',"ULTRAMAR",'CIRCLEK',"MACEWEN","MOBIL","GAS","PETROCAN", 'MRGAS','ESSO','SHELL',"MAC EWEN ","FUEL","PETRO"],
        'Church':["CALVARY CHURCH"],
        'Education':["OPTIONS"],
        "Miscellaneous Payement": [
            "Returned Payment",
            'REFUNDED'
        ],
        "Miscellaneous Charges": [
            "PARKSMART",
            "IMPARK00110003U",
            'MONTHLY FEES',
            "Dishonoured Payment",
            "PAYBYPHONE",
            "NSF ",
            "PARKING",
            "INDIGO PARK",
            "HOTEL PONTIAC",
            "Place D'orlans",
            "NCC- VINCENT MASSEY PA "
            ,"Opl/Bpo",

            "PREMIUM"
         
        ]
    }
def loadList():
    parsers =[]
    parsers.append(scotiaParser)
    parsers.append(americianExpressParser)
    parsers.append(CBSAPayHistory)
    parsers.append(tangerineParser)
    parsers.append(simpliCreditParser)

    parsers.append(wealthSimple)
    return parsers


def parse():


    if os.path.exists(WORK_FILE):
        df = pd.read_csv(WORK_FILE)
    else:
    
        parsedData=[]
        unparsed_files = []
        parsers= loadList()

        # Loop through each file in the directory
        for filename in os.listdir(DATA_DIR):
            filepath = os.path.join(DATA_DIR, filename)

            found_parser = False

            #check if a parser can parse it 
            for parse in parsers:
                if parse.canParse(filepath):
                    parsedData.append(parse.parse(filepath))
                    found_parser = True
                    break  # Exit the loop once a parser is found

            if not found_parser:
                unparsed_files.append(filepath)  # Add the file to the list of unparsed files
        
        # Concatenate all DataFrames in 'parsedData' into a single DataFrame
        df = pd.concat(parsedData, axis=0, ignore_index=True)

        df[MODEL_DATE] = pd.to_datetime(df[MODEL_DATE] ) 
        addCategorize(df)
        df.to_csv(WORK_FILE, index=False)

    df[MODEL_DESCRIPTION] = df[MODEL_DESCRIPTION].str.strip()
    df[MODEL_DATE] = pd.to_datetime(df[MODEL_DATE] ) 
    #fitler by 2023
    df = df[df[MODEL_DATE].dt.year ==  YEAR]
   
    items = df.to_dict(orient='records')

    parseTranscationsCatogeryByMonth(df)
    output= 'output.xlsx'
    log.info("Saving results to "+ output)
    df.to_excel(output, index=True)

    log.info("The results of the unknown records :")
    viewUnknownRecords(df)

   


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
            if(row[MODEL_DESCRIPTION].upper().strip().find(keyword.upper().strip())>-1):
                    return category      
    return 'Unknown'

def parseExpenseByMonth(df):
    expense = df[df[MODEL_AMOUNT] < 0]
    expense_by_month_year = expense.groupby([expense[MODEL_DATE].dt.year, expense[MODEL_DATE].dt.month,MODEL_CATEGORY])[MODEL_AMOUNT].sum()

    # print the aggregated income by month and year
    log.info(expense_by_month_year)


def parseExpenseCatogeryByMonth(df):
    expense = df[df[MODEL_AMOUNT] < 0]


    # Group the data by month, year, and category, and sum the 'Amount' column
    expense_by_month_year = expense.groupby([
        MODEL_CATEGORY,
        expense[MODEL_DATE].dt.year,
        expense[MODEL_DATE].dt.strftime('%B')  # Format the month as "Month"
    ])[MODEL_AMOUNT].sum()
    # print the aggregated income by month and year

    printResults(expense_by_month_year)


def parseTranscationsCatogeryByMonth(df):
    # Assuming MODEL_CATEGORY, MODEL_DATE, and MODEL_AMOUNT are defined elsewhere
    #assume that data has only one year of data
    
    # Group the data by month, year, and category, and sum the 'Amount' column
    expense_by_month_year = df.groupby([
        MODEL_CATEGORY,
        df[MODEL_DATE].dt.strftime('%B')  # Format the month as "Month"
    ])[MODEL_AMOUNT].sum()
    
    # Print the aggregated income by month and year
    printResults(expense_by_month_year)
    
    # Convert the grouped data to a DataFrame
    expense_by_month_year_df = expense_by_month_year.reset_index()
    pivot_df = expense_by_month_year_df.pivot_table(index=MODEL_CATEGORY, columns=[ MODEL_DATE], values=MODEL_AMOUNT, aggfunc='sum')
    
    # Convert negative values to positive
    pivot_df = pivot_df.abs()

    # Reorder the columns based on the chronological order of months
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    pivot_df = pivot_df.reindex(columns=months_order, level=0)

    # Save the pivoted DataFrame to an Excel file
    pivot_df.to_excel('expense_by_month_year.xlsx')


def parseExpenseCategoryByYear(df):

   # group the data by month and year, and sum the income
    expense = df[df[MODEL_AMOUNT] < 0]
     # Group the data by month, year, and category, and sum the 'Amount' column
    expense_by_year = expense.groupby([MODEL_CATEGORY,expense[MODEL_DATE].dt.year])[MODEL_AMOUNT].sum()

    # print the aggregated income by month and year
    log.info(expense_by_year)

def viewUnknownRecords(df):
    category_to_filter = 'Unknown'

    # Filter the DataFrame to get records with the specific category
    filtered_expense = df[df[MODEL_CATEGORY] == category_to_filter]

    printUniqueNames(filtered_expense)

def parseExpenseByYear(df):

   # group the data by month and year, and sum the income
    expense = df[df[MODEL_AMOUNT] < 0]
    expense_by_year = expense.groupby([expense[MODEL_DATE].dt.year])[MODEL_AMOUNT].sum()

    # print the aggregated income by month and year
    log.info(expense_by_year)

def parseTranscationByYear(df):

   # group the data by month and year, and sum the income
    transcations = df[df[MODEL_AMOUNT] < 0]
    transcations_by_year = transcations.groupby([transcations[MODEL_DATE].dt.year])[MODEL_AMOUNT].sum()

    # print the aggregated income by month and year
    log.info(transcations_by_year)

if __name__ == "__main__":
    parse()