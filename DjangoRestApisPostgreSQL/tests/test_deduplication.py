import os
import pandas as pd
import shutil
from datetime import datetime
from budget.processing import process_files
from config import DATA_DIR, WORK_FILE, MODEL_DATE, MODEL_DESCRIPTION, MODEL_AMOUNT

# --- Setup Test Data ---
def setup_test_environment():
    """Creates a temporary test environment with sample CSV files."""
    # Ensure DATA_DIR exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Sample data for file 1
    data_1 = pd.DataFrame({
        MODEL_DATE: [datetime(2025, 1, 15), datetime(2025, 1, 16)],
        MODEL_DESCRIPTION: ["Coffee Shop", "Grocery Store"],
        MODEL_AMOUNT: [-5.75, -40.12]
    })
    file_1 = os.path.join(DATA_DIR, "test_file_1.csv")
    data_1.to_csv(file_1, index=False)

    # Duplicate of file 1 (simulates re-downloaded statement)
    file_2 = os.path.join(DATA_DIR, "test_file_2.csv")
    data_1.to_csv(file_2, index=False)

    # Another file with one duplicate row and one new row
    data_2 = pd.DataFrame({
        MODEL_DATE: [datetime(2025, 1, 15), datetime(2025, 1, 20)],
        MODEL_DESCRIPTION: ["Coffee Shop", "Online Purchase"],
        MODEL_AMOUNT: [-5.75, -100.00]
    })
    file_3 = os.path.join(DATA_DIR, "test_file_3.csv")
    data_2.to_csv(file_3, index=False)

    return [file_1, file_2, file_3]


def teardown_test_environment(files):
    """Cleans up the test environment."""
    for file in files:
        if os.path.exists(file):
            os.remove(file)
    if os.path.exists(WORK_FILE):
        os.remove(WORK_FILE)


# --- Main Test Runner ---
def run_test():
    print("🔧 Setting up test environment...")
    files = setup_test_environment()

    print("🚀 Running process_files()...")
    df = process_files()

    print("\n📊 Final Processed DataFrame:")
    print(df)

    print("\n✅ Verifying Deduplication...")
    assert len(df) == 3, f"Expected 3 unique rows, got {len(df)}"
    assert df[MODEL_DESCRIPTION].nunique() == 3, "Descriptions should all be unique after deduplication"

    print("🎉 TEST PASSED — Deduplication works as expected.")

    teardown_test_environment(files)


if __name__ == "__main__":
    run_test()
