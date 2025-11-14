import pandas as pd
from parsers import amexParser

def test_parse_amex(tmp_path, amex_csv_content):
    test_file = tmp_path / "amex_statement.CSV"
    test_file.write_text(amex_csv_content)

    df = amexParser.parse(str(test_file))

    assert set(df.columns) == {"Date", "Description", "Amount", "Origin"}
    assert df.iloc[1]["Description"] == "Amazon"
    assert df.iloc[1]["Amount"] == -120.99