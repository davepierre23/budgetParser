

import pandas as pd
import os
import logging as log

import scotiaParser
import americianExpressParser
import simpliCreditParser
import CBSAPayHistory
import tangerineParser
import wealthSimple
import calendar
import wiseParser
from pathlib import Path

# Absolute path, raw string style:
DATA_DIR = r"C:\Users\davep\Documents\budget\DjangoRestApisPostgreSQL\budget\data"

# Configuration
log.basicConfig(format="%(message)s", level=log.INFO)
WORK_FILE = "my_data.csv"

MODEL_DATE = "Date"
MODEL_DESCRIPTION = "Description"
MODEL_AMOUNT = "Amount"
MODEL_ORIGIN = "Origin"
MODEL_CATEGORY = "Category"

YEAR = 2025

# Define categories based on keywords in the "Description" column

categories = {
    "Wealthsimple": ["Wealthsimple"],
    
    "Alcohol": ["LCBO/RAO", "PURE BREW"],

    "Groceries": [
        "TooGoodT", "FLASHFOOD", "HALIBUT HOUSE", "WALMART.CA", "FRESHCO", "BULK BARN", "DUNKIN",
        "REVOLUTIONN", "NO FRILLS", "FOOD BASICS", "METRO", "SOBEYS", "LOBLAWS", "WAL*MART", "CHAP CHAP SNACKS Ottawa",
        "NSEYA'S", "Shoppers Drug Mart", "FARM BOY", "REXALL", "YIG", "T&T", "CANADIAN TIRE"
    ],

    "Restaurants": [
        "MIKE DEAN'S", "Cafe", "LITTLE CAESARS", "ROYAL OAK", "BOOSTER JUICE", "CORA", "HALIBUT",
        "TIPIKLIZ", "HARVEY", "LEVEL ONE", "DAIRY QUEEN", "SHOELESS JOES", "Subway", "FOOD",
        "PITA BELL KABAB", "Chances", "SHAWARMA PALACE", "WENDYS", "LOUIS", "JONNY CANUCK'S",
        "CAFÉ LATTE", "NOM NOM", "PRESOTEA", "HEY KITCHEN", "MEZZANOTTE", "A&W", "BAKERY",
        "DOUGHNUTS", "JACK ASTOR'S", "MCDONALD'S", "DOORDASH", "Seoul Dog", "PIZZERIA",
        "FAIRMONT CHATEAU LAURIE", "COBS BREAD", "MILKMAN", "SUSHI", "BRIG", "LEXINGTON SMOKEHOUSE",
        "CHICK-FIL-A", "KFC", "FRUIT", "BROADWAY", "DELICIOUS STEAKHOUSE", "TIM HORTONS",
        "STARBUCKS", "LUNCHBOX", "Wild Wing", "THE ALLEY", "GYUBEE", "RED LOBSTER", "MENCHIE",
        "SQ *PANCHO'S", "DAOL", "SOUL STONE", "MR. PRETZEL", "METROPOLITAIN", "St. Louis Bar",
        "Bagel", "COCO FRESH TEA", "LE ST LAURENT", "MAVERICK'S", "POPEYES", "Chatime", "SHAKER",
        "MARY BROWN'S", "SUSHI KAN", "MANDARIN", "SHOPPERS", "LE MIEN", "JOLLIBEE-", "MOXIES",
        "AZTEC", "GREEN FRESH", "TEALIVE", "BOSTON PIZZA", "EAST SIDE MARIO", "Pizza Pizza",
        "THE GREAT CANADIAN PO", "Carleton Web", "UBER EATS", "BIG BONE BBQ","SKIPTHEDISHES"
    ],

    "Clothing": [
        "Tip Top", "SPORT CHEK", "WINNERS", "ADIDAS", "SPORTS", "OLD NAVY", "THE GAP",
        "FAIRWEATHER", "THREADS TAILORS", "Shoe Company", "SP JOJIKA", "SHEIN", "VALUE VILLAGE",
        "OVO", "BOATHOUSE", "LEZE THE LABEL"
    ],

    "Entertainment": [
        "DOOLY'S OTTAWA INC. OTTAWA ON", "DISNEYPLUS", "GOLF", "FALCON RIDGE", "PUTTING EDGE",
        "NORDIK", "TEE 2 GREEN", "DOLLYS", "STEAM", "PHD IN WAVES", "CALYPSO", "TICKET",
        "SMASH ROOM", "LANDMARK", "WHITE SANDS", "Orleans Bowling.com", "BOWLING",
        "Top Karting Hull", "Sunrise Records", "SP TSX1", "eBay", "GAMESTOP", "CARTA", "EB *ALL FALLS DOWN FIL TORONTO"
        "Canada Computers", "PLAYSTATION", "RED DRAGON", "VRADVENTURES.ZONE", "VR ADVENTURES.ZONE",
        "EVENTBRITE", "TCGPLAYER", "TCGPLAYER.COM", "401 GAMES", "Wtbmatters", "Monkey Kart","Entertain St991",
        "Teamlab Planets Tokyo", "Crypto Arena Mercandise", "HIPSTER LASERS", "WEEB MANIA", "SWIMPLY","Anchor Night Club"
    ],

    "Car Loan": ["Loan Payment", "BANK STREET MAZDA"],

    "Car Maintenance": ["OIL CHANGERS", "Caps Auto", "CARLING TIRE"],

    "Travel": [
        "Hopper",
        "Airlines", "FLIGHTHUB", "AIRBNB", "Caltrain","AIRCANADA", "HOPPER", "KLOOK TRAVEL TECH", "KLOOK",
        "JRC SHINKANSEN", "CALTRAIN", "MOXY DWNTN LOS ANGEL", "THE HOXTON", "GUEST SERVICES OF",
        "JRC SMART EX TOKYO", "RADICAL TOKYO", "SEVEN-ELEVEN", "MEGADONQUIJOTE", "TEAMLAB PLANETS"
    ],

    "Travel": ["MOXY DWNTN LOS ANGEL", "AIRBnb" , "AIRCANADA", "AIRLINES","KLOOK","THE HOXTON", "FAIRMONT CHATEAU", "HOTEL PONTIAC", "AIRALO ", "CAA NORTH"],

    "Subscriptions": ["DISNEYPLUS", "MEMBERSHIP FEE INSTALLMENT", "NETFLIX"],

    "Car Insurance": ["BELAIR INS/ASS", "BELAIRDIRECT", "BELAIR"],

    "Online Shopping": [
        "LEGO", "JEWELLERS", "HIVEMAPPER", "MY USADDRESS", "AFROBLAST", "SIMPLYMODBOX",
        "AMZN", "AMAZON", "APPLE", "SNAPLII" 
    ],

    "Transportation": [
        "Uber", "Ubr*", "Lyft", "PRESTO", "PPARK", "BUSBUD","Mto Tsd ", "QP ORLEANS", "IMPARK", "PARKING"
    ],

    "Doctors/Dental/Vision": [
        "APPLE'S CROWN", "ACE OF SPADES", "CLEARVIEW", "KITS", "Echo", "LASIK MD", "PHYSIO",
        "HUNTER CHIROPRACTIC", "TENTH LINE PHARMACY"
    ],

    "Personal Care": [
        "CLORE", "MONTEGO", "MONAT", "NANCY'S NAILS AND LASHE", "BATH & BODY WORKS"
    ],

    "Gym": ["SHOWCASE", "SP CROSSROPE", "FIT4LESS", "OTTAWACITY"],

    "Home Goods": [
        "QUICK PICK", "Dollarama", "PANDABUY", "BEST BUY", "DOLLAR TREE", "GIANT TIGER",
        "CDN TIRE", "HUDSON'S BAY", "WAL-MART", "Kylescouter", "CANADIANTIRE"
    ],

    "Income": ["Basic Pay", "Acting / Appointment Pay"],

    "Gas": [
        "PIONEER", "ULTRAMAR", "CIRCLEK", "MACEWEN", "MOBIL", "GAS", "PETROCAN", "MRGAS",
        "ESSO", "SHELL", "MAC EWEN", "FUEL", "PETRO"
    ],

    "Church": ["CALVARY CHURCH"],

    "Education": ["OPTIONS", "R.I.S.E. ACADEMY", "The Aqua Life Swim Sch"],

    "Miscellaneous Payment": [
        "Returned Payment", "REFUNDED"
    ],

    "Miscellaneous Charges": [
        "PARKSMART", "IMPARK00110003U", "MONTHLY FEES", "Dishonoured Payment", "PAYBYPHONE",
        "NSF", "PARKING", "INDIGO PARK", "HOTEL PONTIAC", "Place D'orlans", "NCC- VINCENT MASSEY PA",
        "Opl/Bpo", "PREMIUM"
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
        wiseParser
    ]


def categorize(row):
    """Categorize transactions based on description."""
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.upper()in row[MODEL_DESCRIPTION].upper():
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

def load_data():
    if os.path.exists(WORK_FILE):
        df = pd.read_csv(WORK_FILE)
    else:
        log.error("Data file not found!")
        return None

    df[MODEL_DATE] = pd.to_datetime(df[MODEL_DATE])
    df = df[df[MODEL_DATE].dt.year == YEAR]
    return df

def add_categories(df):
    df[MODEL_CATEGORY] = df.apply(categorize, axis=1)
    return df
def calculate_metrics(df):
    # Total income and expenses
    total_income = df[df[MODEL_AMOUNT] > 0][MODEL_AMOUNT].sum()
    total_expense = df[df[MODEL_AMOUNT] < 0][MODEL_AMOUNT].sum()
    net_savings = total_income + total_expense

    # Monthly metrics
    monthly_expense = df[df[MODEL_AMOUNT] < 0].groupby(df[MODEL_DATE].dt.month)[MODEL_AMOUNT].sum()
    monthly_expense_by_category = df[df[MODEL_AMOUNT] < 0].groupby([df[MODEL_DATE].dt.month, MODEL_CATEGORY])[MODEL_AMOUNT].sum()

    # Largest and smallest spending months
    largest_spending_month =monthly_expense.idxmax() 
    smallest_spending_month = monthly_expense.idxmin()

    # Fun facts
    biggest_splurge = df[df[MODEL_AMOUNT] < 0][MODEL_AMOUNT].min()
    smallest_purchase = df[df[MODEL_AMOUNT] < 0][MODEL_AMOUNT].max()


    
    # Find the most frequent vendor
    most_frequent_vendor = df[MODEL_DESCRIPTION].value_counts().idxmax()

    # Filter rows for the most frequent vendor
    vendor_rows = df[df[MODEL_DESCRIPTION] == most_frequent_vendor]

    # Calculate the total value spent on this vendor
    total_spent_on_vendor = vendor_rows[MODEL_AMOUNT].sum()

    # Print the results
    print(f"Total amount spent on {most_frequent_vendor}: {total_spent_on_vendor}")


      # Largest and smallest spending month
    monthly_expenses = df[df[MODEL_AMOUNT] < 0].groupby(df[MODEL_DATE].dt.month)[MODEL_AMOUNT].sum()
    largest_month = monthly_expenses.idxmin()
    smallest_month = monthly_expenses.idxmax()
    largest_month_spending = monthly_expenses.min()
    smallest_month_spending = monthly_expenses.max()

    # Convert to month names
    largest_month_name = calendar.month_name[largest_month]
    smallest_month_name = calendar.month_name[smallest_month]

    print(f"Largest Spending Month: {largest_month_name} with total spending of ${largest_month_spending:.2f}")
    print(f"Smallest Spending Month: {smallest_month_name} with total spending of ${smallest_month_spending:.2f}")

    # Biggest splurge
    biggest_splurge_row = df[df[MODEL_AMOUNT] < 0].nsmallest(1, MODEL_AMOUNT).iloc[0]
    biggest_splurge_description = biggest_splurge_row[MODEL_DESCRIPTION]
    biggest_splurge_amount = biggest_splurge_row[MODEL_AMOUNT]

    print(f"Biggest Splurge: {biggest_splurge_description} with an amount of ${abs(biggest_splurge_amount):.2f}")

    expense_df = df[df[MODEL_AMOUNT] < 0]
    income_df = df[df[MODEL_AMOUNT] > 0]

    # 1. Top Spending Day
    top_spending_day = expense_df.groupby(MODEL_DATE)[MODEL_AMOUNT].sum().idxmin()
    top_spending_day_amount = expense_df.groupby(MODEL_DATE)[MODEL_AMOUNT].sum().min()
    log.info(f"Top Spending Day: {top_spending_day.strftime('%B %d, %Y')} with total spending of ${abs(top_spending_day_amount):.2f}")

    # 2. Best Month (Savings)
    savings_by_month = df.groupby(df[MODEL_DATE].dt.strftime('%B'))[MODEL_AMOUNT].sum()
    best_savings_month = savings_by_month.idxmax()
    best_savings_amount = savings_by_month.max()
    log.info(f"Best Month (Savings): {best_savings_month} with net savings of ${best_savings_amount:.2f}")

    # 3. Most Consistent Category
    consistent_categories = expense_df.groupby(MODEL_CATEGORY).nunique()[MODEL_DATE]
    most_consistent_category = consistent_categories.idxmax()
    log.info(f"Most Consistent Category: {most_consistent_category}")

    # 4. Favorite Payment Method (if payment data exists)
    if MODEL_ORIGIN in df.columns:
        favorite_payment_method = df[MODEL_ORIGIN].value_counts().idxmax()
        log.info(f"Favorite Payment Method: {favorite_payment_method}")

    # 5. Longest No-Spend Streak
    no_spend_streak = (expense_df[MODEL_DATE].diff().dt.days > 1).astype(int).cumsum()
    longest_streak_days = no_spend_streak.value_counts().max()
    log.info(f"Longest No-Spend Streak: {longest_streak_days} days")

    # 6. "You Could Have Saved"
    non_essential_categories = ['Entertainment', 'Restaurents']
    non_essential_spending = expense_df[expense_df[MODEL_CATEGORY].isin(non_essential_categories)][MODEL_AMOUNT].sum()
    potential_savings = non_essential_spending * 0.10
    log.info(f"You Could Have Saved: ${abs(potential_savings):.2f} by reducing non-essential spending by 10%.")

    # 7. Impulse Purchase Highlight
    impulse_category = 'Entertainment'
    impulse_purchases = expense_df[expense_df[MODEL_CATEGORY] == impulse_category]
    if not impulse_purchases.empty:
        top_impulse_purchase = impulse_purchases.loc[impulse_purchases[MODEL_AMOUNT].idxmin()]
        log.info(f"Impulse Purchase Highlight: {top_impulse_purchase[MODEL_DESCRIPTION]} for ${abs(top_impulse_purchase[MODEL_AMOUNT]):.2f}")

    # 8. Spending Efficiency
    total_income = income_df[MODEL_AMOUNT].sum()
    total_expense = abs(expense_df[MODEL_AMOUNT].sum())
    savings_ratio = (total_income - total_expense) / total_income * 100
    log.info(f"Spending Efficiency: {savings_ratio:.2f}% of your income was saved.")


      # 9. Top 3 Vendors
    top_vendors = expense_df[MODEL_DESCRIPTION].value_counts().head(3)
    log.info("Top 3 Vendors:")
    for vendor, count in top_vendors.items():
        total_spent = expense_df[expense_df[MODEL_DESCRIPTION] == vendor][MODEL_AMOUNT].sum()
        log.info(f"- {vendor}: {count} transactions, Total Spent: ${abs(total_spent):.2f}")

    # 10. Month-on-Month Change
    expense_by_month = expense_df.groupby(expense_df[MODEL_DATE].dt.to_period('M'))[MODEL_AMOUNT].sum()
    month_on_month_change = expense_by_month.pct_change() * 100
    log.info("Month-on-Month Change in Expenses:")
    for month, change in month_on_month_change.items():
        if pd.notna(change):
            log.info(f"- {month}: {change:.2f}%")




    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_savings": net_savings,
        "monthly_expense": monthly_expense,
        "monthly_expense_by_category": monthly_expense_by_category,
        "largest_spending_month": largest_spending_month,
        "smallest_spending_month": smallest_spending_month,
        "biggest_splurge": biggest_splurge,
        "smallest_purchase": smallest_purchase,
        "most_frequent_vendor": most_frequent_vendor
    }


  

def print_wrapup(metrics):
    log.info("\nYour 2025 Financial Wrapped")
    log.info(f"💸 Total Spent: ${-metrics['total_expense']:.2f}")
    log.info(f"💰 Total Income: ${metrics['total_income']:.2f}")
    log.info(f"📈 Net Savings: ${metrics['net_savings']:.2f}")
    log.info(f"📅 Largest Spending Month: {metrics['largest_spending_month']}")
    log.info(f"📅 Smallest Spending Month: {metrics['smallest_spending_month']}")
    log.info(f"🎯 Biggest Splurge: ${-metrics['biggest_splurge']:.2f}")
    log.info(f"☕ Most Frequent Vendor: {metrics['most_frequent_vendor']}")

def save_monthly_expense_by_category(metrics):
    pivot_df = metrics['monthly_expense_by_category'].unstack().fillna(0)
    pivot_df.to_excel('monthly_expense_by_category.xlsx')


def main():
    df = load_data()
    if df is None:
        return

    df = add_categories(df)
    metrics = calculate_metrics(df)
    print_wrapup(metrics)
    save_monthly_expense_by_category(metrics)




def print_unknown_transactions(path):
    """
    Read a CSV, keep rows whose Category == 'Unknown', and
    print Date, Description, Amount, Origin, Category.
    """
    df = pd.read_csv(path, dtype=str)          # ← read_csv, not read_excel
    mask = df["Category"].str.lower().eq("unknown")
    unknown_rows = df.loc[mask, ["Date", "Description", "Amount", "Origin", "Category"]]

    if unknown_rows.empty:
        print("✅ No transactions with Category = 'Unknown'.")
    else:
        print(unknown_rows.to_string(index=False))
 

#

if __name__ == "__main__":
    process_files() 
    main()

    print_unknown_transactions(WORK_FILE)
