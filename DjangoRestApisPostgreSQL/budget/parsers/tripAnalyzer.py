import pandas as pd
import logging as log
log.basicConfig(format='%(message)s', level=log.INFO)

MODEL_DATE = 'Date'
MODEL_DESCRIPTION = 'Description'
MODEL_AMOUNT = 'Amount'
MODEL_CATEGORY = 'Category'


def analyze_trip(df, trip_name, start_date, end_date, keywords):
    """
    Analyze spending for a given trip.

    Parameters:
    - df: DataFrame with transaction data
    - trip_name: str, name of the trip
    - start_date: str (YYYY-MM-DD), start of trip
    - end_date: str (YYYY-MM-DD), end of trip
    - keywords: list of str, keywords to identify trip-related transactions
    """
    df[MODEL_DATE] = pd.to_datetime(df[MODEL_DATE])

    trip_df = df[
        (df[MODEL_DATE] >= pd.to_datetime(start_date)) &
        (df[MODEL_DATE] <= pd.to_datetime(end_date)) &
        (df[MODEL_DESCRIPTION].str.contains('|'.join(keywords), case=False, na=False))
    ]

    if trip_df.empty:
        log.info(f"No transactions found for trip: {trip_name}")
        return

    log.info(f"\n===== {trip_name} Trip Report =====")
    log.info(f"Total Spent: ${abs(trip_df[MODEL_AMOUNT].sum()):.2f}")

    log.info("\nTop Categories:")
    category_summary = trip_df.groupby(MODEL_CATEGORY)[MODEL_AMOUNT].sum().abs().sort_values(ascending=False)
    for category, amount in category_summary.items():
        log.info(f"  {category}: ${amount:.2f}")

    log.info("\nTop Vendors:")
    top_vendors = trip_df[MODEL_DESCRIPTION].value_counts().head(5)
    for vendor, count in top_vendors.items():
        log.info(f"  {vendor}: {count} transactions")

    log.info("\nDetailed Breakdown:")
    for _, row in trip_df.iterrows():
        log.info(f"  {row[MODEL_DATE].strftime('%Y-%m-%d')}: {row[MODEL_DESCRIPTION]} - ${abs(row[MODEL_AMOUNT]):.2f}")
