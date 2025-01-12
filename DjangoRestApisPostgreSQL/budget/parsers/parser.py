

import pandas as pd
import os
import logging as log

import scotiaParser
import americianExpressParser
import simpliCreditParser
import CBSAPayHistory
import tangerineParser
import wealthSimple

# Configuration
log.basicConfig(format="%(message)s", level=log.INFO)
DATA_DIR = "/Users/davepierre/Documents/Projects/budgetParser/data"
WORK_FILE = "my_data.csv"

MODEL_DATE = "Date"
MODEL_DESCRIPTION = "Description"
MODEL_AMOUNT = "Amount"
MODEL_ORIGIN = "Origin"
MODEL_CATEGORY = "Category"

YEAR = 2024

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

def load_parsers():
    """Load all parsers."""
    return [
        scotiaParser,
        americianExpressParser,
        CBSAPayHistory,
        tangerineParser,
        simpliCreditParser,
        wealthSimple,
    ]


def categorize(row):
    """Categorize transactions based on description."""
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.upper() in row[MODEL_DESCRIPTION].upper():
                return category
    return "Unknown"


def add_category_column(df):
    """Add a category column to the DataFrame."""
    df[MODEL_CATEGORY] = df.apply(categorize, axis=1)


def process_files():
    """Parse and process transaction files into a unified DataFrame."""
    if os.path.exists(WORK_FILE):
        df = pd.read_csv(WORK_FILE)
    else:
        parsers = load_parsers()
        parsed_data = []
        unparsed_files = []

        for filename in os.listdir(DATA_DIR):
            filepath = os.path.join(DATA_DIR, filename)
            parsed = False

            for parser in parsers:
                if parser.canParse(filepath):
                    parsed_data.append(parser.parse(filepath))
                    parsed = True
                    break

            if not parsed:
                unparsed_files.append(filepath)

        if not parsed_data:
            raise ValueError("No valid data was parsed.")

        df = pd.concat(parsed_data, ignore_index=True)
        df[MODEL_DATE] = pd.to_datetime(df[MODEL_DATE])
        add_category_column(df)
        df.to_csv(WORK_FILE, index=False)

    df[MODEL_DATE] = pd.to_datetime(df[MODEL_DATE])
    return df[df[MODEL_DATE].dt.year == YEAR]


def yearly_summary(df):
    """Generate yearly expense and income summaries with totals and net savings."""
    # Separate expenses and income
    expenses = df[df[MODEL_AMOUNT] < 0]
    income = df[df[MODEL_AMOUNT] > 0]

    # Group and aggregate by category
    expense_summary = (
        expenses.groupby([MODEL_CATEGORY])[MODEL_AMOUNT]
        .sum()
        .sort_values(ascending=False)
    )
    income_summary = (
        income.groupby([MODEL_CATEGORY])[MODEL_AMOUNT]
        .sum()
        .sort_values(ascending=False)
    )

    # Calculate totals
    total_expenses = expenses[MODEL_AMOUNT].sum()
    total_income = income[MODEL_AMOUNT].sum()
    net_savings = total_income + total_expenses  # Add because expenses are negative

    # Log results
    log.info("\nExpense Summary by Category:")
    log.info(expense_summary)
    log.info("\nIncome Summary by Category:")
    log.info(income_summary)
    log.info(f"\nTotal Expenses: {total_expenses:.2f}")
    log.info(f"Total Income: {total_income:.2f}")
    log.info(f"Net Savings: {net_savings:.2f}")

    # Save to Excel
    with pd.ExcelWriter("yearly_summary.xlsx") as writer:
        expense_summary.to_excel(writer, sheet_name="Expenses")
        income_summary.to_excel(writer, sheet_name="Income")

        # Add totals and net savings to a summary sheet
        summary_data = {
            "Metric": ["Total Expenses", "Total Income", "Net Savings"],
            "Amount": [total_expenses, total_income, net_savings],
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name="Summary", index=False)

    log.info("Yearly summary with totals and net savings saved to 'yearly_summary.xlsx'.")



def parse():
    """Main parsing function."""
    df = process_files()
    yearly_summary(df)


if __name__ == "__main__":
    parse()
