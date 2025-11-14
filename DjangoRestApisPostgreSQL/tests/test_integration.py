import pandas as pd
from parsers.tangerine_parser import parse_tangerine
from utils.state_manager import StateManager

def test_pipeline_new_transactions(tmp_path):
    # setup state manager
    state_path = tmp_path / "state.json"
    sm = StateManager(state_path)

    # create fake CSV with 2 transactions
    file = tmp_path / "test.csv"
    file.write_text("Date,Transaction,Name,Memo,Amount\n"
                    "01/01/2025,OTHER,Test1,,100\n"
                    "01/02/2025,OTHER,Test2,,200\n")

    # parse
    df = parse_tangerine(file)
    assert len(df) == 2

    # simulate first run (all transactions are new)
    new_tx = sm.get_new_transactions(df)
    assert len(new_tx) == 2

    # update last_run
    sm.update_last_run("2025-01-02")

    # run again — should return 0 new transactions
    new_tx = sm.get_new_transactions(df)
    assert len(new_tx) == 0
