import pandas as pd
import os
import logging as log
from config import DATA_DIR,WORK_FILE, MASTER_OUT, MODEL_DATE,  MODEL_AMOUNT,  MODEL_DESCRIPTION, MODEL_TRIP, MODEL_CATEGORY

log.basicConfig(format="%(message)s", level=log.INFO)


MASTER_OUT  = "all_trips_tagged.csv"  # combined output

# ── trip definitions (extend freely) ────────────────────────────────────────────
TRIPS = {
    "Japan 2025": {
        "start": "2025-03-21",
        "end":   "2025-04-08",
        "keywords": [
            "Suica", "FamilyMart", "7-Eleven", "Don Quijote", "Tokyo",
            "Osaka", "Kyoto", "Lawson", "Shinkansen", "JR", "Pasmo",
            "JRC", "Megadonquijote", "Teamlab", "Radical Tokyo"
        ],
        "outfile": "japan_trip.csv"
    },
    "LA 2025": {
        "start": "2025-03-17",
        "end":   "2025-03-25",
        "keywords": [
            "Crypto Arena", "Moxy", "The Hoxton", "Uber", "Caltrain",
            "Swimply", "Anchor Night Club", "Radical Tokyo Los Angeles",
            "Guest Services Of", "LAX", "Los Angeles"
        ],
        "outfile": "la_trip.csv"
    },
}

# ── your existing look‑ups (shortened here for brevity) ─────────────────────────
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
# ── helpers ─────────────────────────────────────────────────────────────────────
def in_trip(desc, keywords):
    """Return True if any keyword occurs in description (case‑insensitive)."""
    desc_low = desc.lower()
    return any(k.lower() in desc_low for k in keywords)

def categorize_row(desc):
    for cat, words in categories.items():
        if any(w.lower() in desc.lower() for w in words):
            return cat
    return "Other"

# ── core pipeline ──────────────────────────────────────────────────────────────
def add_trip_tags(df: pd.DataFrame) -> pd.DataFrame:
    """Add a 'Trip' column based on TRIPS dict; leave blank if non‑trip row."""
    df[MODEL_TRIP] = ""         # start empty
    for trip_name, meta in TRIPS.items():
        mask = (
            (df[MODEL_DATE] >= pd.to_datetime(meta["start"])) &
            (df[MODEL_DATE] <= pd.to_datetime(meta["end"]))   &
            (df[MODEL_DESCRIPTION].apply(in_trip, args=(meta["keywords"],)))
        )
        df.loc[mask, MODEL_TRIP] = trip_name
    return df

def main():
    if not os.path.exists(WORK_FILE):
        log.error("CSV data file not found!")
        return

    # 1. Load & clean ----------------------------------------------------------------
    df = pd.read_csv(WORK_FILE)
    df[MODEL_DATE] = pd.to_datetime(df[MODEL_DATE])
    df[MODEL_DESCRIPTION] = df[MODEL_DESCRIPTION].astype(str).str.strip()

    # 2. Normalize vendor names -------------------------------------------------------
    df[MODEL_DESCRIPTION] = df[MODEL_DESCRIPTION].replace(vendor_normalization)

    # 3. Categorize every row (if not already done) -----------------------------------
    if MODEL_CATEGORY not in df.columns or df[MODEL_CATEGORY].isna().all():
        df[MODEL_CATEGORY] = df[MODEL_DESCRIPTION].apply(categorize_row)

    # 4. Tag trips --------------------------------------------------------------------
    df = add_trip_tags(df)

    # 5. Save a single master file ----------------------------------------------------
    df.to_csv(MASTER_OUT, index=False)
    log.info(f"All data with trip tags saved to: {MASTER_OUT}")

    # 6. Optional: split per trip -----------------------------------------------------
    for trip_name, meta in TRIPS.items():
        trip_rows = df[df[MODEL_TRIP] == trip_name]
        if trip_rows.empty:
            log.info(f"No transactions found for «{trip_name}».")
            continue

        outfile = meta["outfile"]
        trip_rows.to_csv(outfile, index=False)
        log.info(f"{trip_name}: {len(trip_rows)} rows ➜ {outfile}")

        # Quick summary
        spent = trip_rows[trip_rows[MODEL_AMOUNT] < 0][MODEL_AMOUNT].sum()
        log.info(f"   → total spent: ${abs(spent):.2f}\n")

if __name__ == "__main__":
    main()
