import pandas as pd
import os
import logging as log

log.basicConfig(format='%(message)s', level=log.INFO)

MODEL_DATE = 'Date'
MODEL_DESCRIPTION = 'Description'
MODEL_AMOUNT = 'Amount'
MODEL_ORIGIN = 'Origin'
MODEL_CATEGORY = 'Category'
WORK_FILE = 'my_data.csv'
OUTPUT_FILE = 'japan_trip.csv'

TRIP_START = pd.to_datetime("2025-03-21")
TRIP_END = pd.to_datetime("2025-04-08")

JAPAN_KEYWORDS = [
    "Suica", "FamilyMart", "7-Eleven", "Don Quijote", "Tokyo", "Osaka", "Kyoto", "Lawson",
    "JPY", "Yen", "Japan", "Kansai", "Narita", "Shinkansen", "IC Card", "IC fare", "JR", "Pasmo"
]

categories = {
    "Transport": [
        "Suica", "Radical Tokyo", "Puraudeko", "Train", "IC fare", "Transit","Subway", "Deiri-Yamazaki",
        "Coin Lockers", "Mv Nankaikishinosato", "Jal Pac", 
    ],
    "Food": [
        "7-Eleven", "FamilyMart", "Lawson", "McDonald's", "Starbucks", "Burger King", "Ransui Cafe",
        "MOS Burger", "Green Beans Parlor", "Mrwaffleandstandakihabara", "Kentatsukifuraidochikin", "Tabe Park",
        "Plusta Bento", "Manafu", "Kakigori Miyanoya", "Ohanabatake Gionten", "Mamemonototaiyaki", "Kyoto Bistro"
    ],
    "Shopping": [
        "Don Quijote", "Yodobashi", "UNIQLO", "Daikoku Drug", "AmiAmi", "Cospa",
        "Eventmb", "MAGNET by SHIBUYA 109", "Owakudanikurotamagokan"
    ],
    "Attractions": [
        "Kyoto Tower", "Temple", "Museum", "Park", "Castle", "Glanta Kyoto", "Oshinohakkaiikemoto", "Anchor"
    ],
    "Accommodation": [
        "Nine Hours", "Nishinari-Ku Osaka-Shi", "Ms Cross Ningyocho", "Kiyomizukimonoya Aya", "Ninehoursningyoutyou"
    ],
    "Borrow": [
        "Jill-Michaela Charles", "Menrika Christian", "Jabber", "Jyuoumujin"
    ],
    "Other": []
}

# Vendor normalization dictionary
vendor_normalization = {
    "Suica Mobile Payment": "Suica",
    "Suica - Mobile pay Apple": "Suica",
    "Lawson - 株式会社ローソン": "Lawson",
    "Jrc Shinkansen": "JRC Shinkansen",
    "JRC SMART EX TOKYO JPN": "JRC Shinkansen",
    "Kyoto Tower Sando": "Kyoto Tower",
    "Glanta Kyoto Ninenzaka": "Glanta Kyoto",
    "Nishinari-Ku Osaka-Shi": "Nine Hours Osaka",
}

def is_japan_trip(description):
    return any(keyword.lower() in description.lower() for keyword in JAPAN_KEYWORDS)

def categorize(description):
    for category, keywords in categories.items():
        if any(keyword.lower() in description.lower() for keyword in keywords):
            return category
    return "Other"

def filter_and_analyze_japan_trip():
    if not os.path.exists(WORK_FILE):
        log.error("CSV data file not found!")
        return

    df = pd.read_csv(WORK_FILE)
    df[MODEL_DATE] = pd.to_datetime(df[MODEL_DATE])
    df[MODEL_DESCRIPTION] = df[MODEL_DESCRIPTION].astype(str).str.strip()

    # Filter by date range, keywords, and origin
    trip_df = df[
        (df[MODEL_DATE] >= TRIP_START) &
        (df[MODEL_DATE] <= TRIP_END) &
        (df[MODEL_DESCRIPTION].apply(is_japan_trip)) 
    ]

    if trip_df.empty:
        log.info("No Japan trip transactions found.")
        return

    # Normalize vendor names
    trip_df[MODEL_DESCRIPTION] = trip_df[MODEL_DESCRIPTION].replace(vendor_normalization)

    # Categorize and sort
    trip_df[MODEL_CATEGORY] = trip_df[MODEL_DESCRIPTION].apply(categorize)
    trip_df = trip_df.sort_values(by=[MODEL_CATEGORY, MODEL_DATE])

    # Save to CSV
    trip_df.to_csv(OUTPUT_FILE, index=False)
    log.info(f"Japan trip transactions saved to: {OUTPUT_FILE}")

    # Summary logs
    log.info("=== Japan Trip Spending Summary (WISE only) ===")
    total_spent = trip_df[trip_df[MODEL_AMOUNT] < 0][MODEL_AMOUNT].sum()
    log.info(f"Total Spent in Japan: ${abs(total_spent):.2f}")

    log.info("Top Vendors (with total spent):")
    top_vendors = trip_df.groupby(MODEL_DESCRIPTION).agg(
        Transactions=('Amount', 'count'),
        TotalSpent=('Amount', lambda x: abs(x[x < 0].sum()))
    ).sort_values(by='Transactions', ascending=False).head(3)

    for vendor, row in top_vendors.iterrows():
        log.info(f" - {vendor}: {row['Transactions']} transactions, ${row['TotalSpent']:.2f} spent")

    log.info("Spending Breakdown by Category:")
    category_totals = trip_df.groupby(MODEL_CATEGORY)[MODEL_AMOUNT].sum()
    for cat, amt in category_totals.items():
        log.info(f" - {cat}: ${abs(amt):.2f}")

if __name__ == "__main__":
    filter_and_analyze_japan_trip()
