# tests/test_full_pipeline.py

import os
import pandas as pd
import pytest
from processing import process_files
from config import MODEL_DATE, MODEL_AMOUNT, MODEL_DESCRIPTION, MODEL_ORIGIN

TEST_DATA_DIR = "tests/data"

def test_process_multiple_files(monkeypatch):
    """Test that multiple input files produce the expected output."""

    # Monkeypatch the DATA_DIR to point to test folder
    monkeypatch.setattr("processing.DATA_DIR", TEST_DATA_DIR)

    df = process_files()
    
    # Basic expectations
    assert isinstance(df, pd.DataFrame)
    assert not df.empty, "The pipeline returned an empty DataFrame"

    # Check no duplicates
    duplicates = df.duplicated(subset=[MODEL_DATE, MODEL_AMOUNT, MODEL_DESCRIPTION])
    assert not duplicates.any(), "Duplicate transactions were not removed"

    # Check no missing values in critical fields
    critical_cols = [MODEL_DATE, MODEL_AMOUNT, MODEL_DESCRIPTION]
    assert not df[critical_cols].isnull().any().any(), "Null values found in critical columns"

def test_handles_empty_file(monkeypatch, tmp_path):
    """Test that an empty file doesn't crash the pipeline."""

    # Create an empty CSV file
    empty_file = tmp_path / "empty_file.csv"
    empty_file.write_text("")

    # Patch DATA_DIR to point to tmp dir containing empty file
    monkeypatch.setattr("processing.DATA_DIR", tmp_path)

    # Process files should not crash, should return empty DF
    df = process_files()
    assert isinstance(df, pd.DataFrame)
    assert df.empty, "Pipeline should return empty DataFrame for empty file"
