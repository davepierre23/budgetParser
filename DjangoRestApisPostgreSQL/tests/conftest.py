import pytest

@pytest.fixture
def tangerine_csv_content():
    return """Date,Name,Amount
2024-01-01,INTERAC e-Transfer,-50.00
2024-01-02,Grocery,-100.00
"""

@pytest.fixture
def amex_csv_content():
    return """Date,Description,Amount
2024-02-01,Coffee,-5.25
2024-02-03,Amazon,-120.99
"""

@pytest.fixture
def scotia_csv_content():
    return """Transaction Date,Details,Debit
2024-03-01,Salary,2000.00111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
2024-03-02,ATM Withdrawal,-200.00
"""
