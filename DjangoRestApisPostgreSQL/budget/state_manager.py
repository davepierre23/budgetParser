# state_manager.py
import json
import os
from datetime import datetime
from config import EXPORT_DIR

STATE_FILE = os.path.join(EXPORT_DIR, "pipeline_state.json")

def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def update_last_run():
    state = load_state()
    state["last_run"] = datetime.now().isoformat()
    save_state(state)

def update_last_download(file_path):
    state = load_state()
    state.setdefault("downloads", {})
    timestamp = os.path.getmtime(file_path)
    file_modified = datetime.fromtimestamp(timestamp).isoformat()
    state["downloads"][file_path] = file_modified
    save_state(state)
    print(f"✅ Recorded {file_path} as last modified {file_modified}")

def should_import(file_path):
    state = load_state()
    downloads = state.get("downloads", {})
    last_logged = downloads.get(file_path)
    file_modified = datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
    return last_logged is None or file_modified > last_logged


import pandas as pd
from datetime import datetime

def get_new_transactions(df, model_date_col: str):
    """
    Given a DataFrame, return only the transactions newer than the last run.
    """
    state = load_state()
    last_run = state.get("last_run")

    if last_run:
        last_run_dt = datetime.fromisoformat(last_run)
        df = df[df[model_date_col] > last_run_dt]

    return df
