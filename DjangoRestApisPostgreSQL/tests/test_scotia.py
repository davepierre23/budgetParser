import pandas as pd
from parsers import scotiaParser

def test_parse_scotia(tmp_path, scotia_csv_content):
    test_file = tmp_path / "scotia.CSV"
    test_file.write_text(scotia_csv_content)

    df = scotiaParser.parse(str(test_file))

    assert "Date" in df.columns
    assert "Amount" in df.columns
    assert "Description" in df.columns
    assert df.iloc[0]["Amount"] == 2000.00
