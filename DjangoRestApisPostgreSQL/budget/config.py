from pathlib import Path
import os

BASE_DIR = os.path.dirname(__file__)
EXPORT_DIR = os.path.join(BASE_DIR, "exports")

DATA_DIR = Path(r"C:\Users\davep\Documents\budgetParser\budgetParser\DjangoRestApisPostgreSQL\budget\data")
#DATA_DIR = Path(r"C:\Users\davep\Downloads\ParentsBankStatement")
CATEGORY_FILE= Path(r"C:\Users\davep\Documents\budgetParser\budgetParser\DjangoRestApisPostgreSQL\budget\categories.py")
WORK_FILE = os.path.join(EXPORT_DIR, "my_data2025.csv") 
YEAR = 2025

MASTER_OUT  = "all_trips_tagged.csv"  # combined output                                                       
MODEL_DATE = "Date"
MODEL_DESCRIPTION = "Description"
MODEL_AMOUNT = "Amount"
MODEL_ORIGIN = "Origin"
MODEL_CATEGORY = "Category"
MODEL_TRIP        = "Trip"   
MODEL_SOURCE ="source_file"
MODEL_CLEAN_DESCRIPT = "CleanDescription"

# Categories dictionary
from categories import categories
