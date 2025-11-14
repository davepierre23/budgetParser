import pandas as pd
from processing import process_files

def test_process_files_with_mixed_parsers(tmp_path, tangerine_csv_content, amex_csv_content):
    # Write fake bank files into tmp_path
    tangerine_file = tmp_path / "4012914604.CSV"
    tangerine_file.write_text(tangerine_csv_content)

    amex_file = tmp_path / "amex_statement.CSV"
    amex_file.write_text(amex_csv_content)

    df = process_files(data_dir=str(tmp_path))

    # Should merge transactions from multiple sources
    assert "Origin" in df.columns
    assert len(df) == 4
    assert set(df["Origin"].unique()) >= {"Tangerine", "Amex"}
