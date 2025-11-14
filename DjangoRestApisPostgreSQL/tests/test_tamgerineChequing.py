import pandas as pd
from parsers import tangerineCheque

def test_parse_tangerine(tmp_path, tangerine_csv_content):
    test_file = tmp_path / "4012914604.CSV"
    test_file.write_text(tangerine_csv_content)

    df = tangerineCheque.parse(str(test_file))

    # Ensure schema is standardized
    assert set(df.columns) == {"Date", "Description", "Amount", "Origin"}
    assert df.iloc[0]["Origin"] == "Tangerine"
    assert isinstance(df.iloc[0]["Date"], pd.Timestamp)
    assert df.iloc[0]["Amount"] == -50.00
