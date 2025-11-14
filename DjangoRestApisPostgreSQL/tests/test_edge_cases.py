import pytest
import pandas as pd
from parsers.tangerine_parser import parse_tangerine

def test_empty_file(tmp_path):
    file = tmp_path / "empty.csv"
    file.write_text("Date,Transaction,Name,Memo,Amount\n")  # only header
    df = parse_tangerine(file)
    assert df.empty

def test_corrupted_file(tmp_path):
    file = tmp_path / "corrupted.csv"
    file.write_text("NotAColumn,Something\n2025-01-01,BadData")
    with pytest.raises(Exception):
        parse_tangerine(file)

def test_date_formats(tmp_path):
    file = tmp_path / "dates.csv"
    file.write_text("Date,Transaction,Name,Memo,Amount\n01/01/2025,OTHER,Test,,100\n2025-01-02,OTHER,Test,,200")
    df = parse_tangerine(file)
    assert pd.api.types.is_datetime64_any_dtype(df["Date"])
