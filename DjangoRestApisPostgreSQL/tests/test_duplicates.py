import pandas as pd
from parsers.tangerine_parser import parse_tangerine


def test_duplicate_transactions(tmp_path):
    file = tmp_path / "dupes.csv"
    file.write_text(
        "Date,Transaction,Name,Memo,Amount\n"
        "01/01/2025,OTHER,Test,,100\n"
        "01/01/2025,OTHER,Test,,100\n"  # duplicate
    )

    df = parse_tangerine(file)

    # Parser should auto-clean duplicates
    assert len(df) == 1
