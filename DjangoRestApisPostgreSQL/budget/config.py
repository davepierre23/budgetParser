from pathlib import Path

DATA_DIR = Path(r"C:\Users\davep\Documents\budgetParser\budgetParser\DjangoRestApisPostgreSQL\budget\data")
WORK_FILE = "my_data2025.csv"
YEAR = 2025

MASTER_OUT  = "all_trips_tagged.csv"  # combined output                                                       
MODEL_DATE = "Date"
MODEL_DESCRIPTION = "Description"
MODEL_AMOUNT = "Amount"
MODEL_ORIGIN = "Origin"
MODEL_CATEGORY = "Category"
MODEL_TRIP        = "Trip"        
# Categories dictionary
from categories import categories
