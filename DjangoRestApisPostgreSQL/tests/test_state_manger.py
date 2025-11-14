import pandas as pd
from state_manager import save_state, load_state, get_new_transactions

def test_state_save_and_load(tmp_path):
    state_file = tmp_path / "state.json"
    state_data = {"last_run": "2024-01-15"}

    save_state(state_file, state_data)
    loaded = load_state(state_file)

    assert loaded == state_data

def test_get_new_transactions():
    df = pd.DataFrame({
        "Date": pd.to_datetime(["2024-01-01", "2024-02-01", "2024-03-01"]),
        "Description": ["A", "B", "C"],
        "Amount": [10, -20, 30],
        "Origin": ["Test", "Test", "Test"]
    })

    new_df = get_new_transactions(df, last_run_date="2024-01-31")

    assert len(new_df) == 2
    assert all(new_df["Date"] > "2024-01-31")
import pytest
import json
from utils.state_manager import StateManager

def test_missing_state_file(tmp_path):
    path = tmp_path / "state.json"
    sm = StateManager(path)
    assert sm.last_run is None  # should initialize cleanly

def test_update_last_run(tmp_path):
    path = tmp_path / "state.json"
    sm = StateManager(path)
    sm.update_last_run("2025-01-01")
    assert sm.last_run == "2025-01-01"
    # reload to confirm persistence
    sm2 = StateManager(path)
    assert sm2.last_run == "2025-01-01"

def test_future_date(tmp_path):
    path = tmp_path / "state.json"
    sm = StateManager(path)
    sm.update_last_run("2100-01-01")
    assert sm.get_new_transactions([]) == []  # no transactions in future
