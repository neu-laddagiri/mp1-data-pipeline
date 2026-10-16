# tests/conftest.py
from pathlib import Path
import pandas as pd
import pytest


@pytest.fixture
def sample_df():
    """Read the existing MP1 sample CSV for each test."""
    filepath = Path("fixtures") / "sample_data.csv"
    return pd.read_csv(filepath)