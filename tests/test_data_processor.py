# tests/test_data_processor.py

import pandas as pd
import pytest

from src.data_processor import handle_missing, remove_duplicates, remove_outliers


def test_remove_duplicates(sample_df):
    result = remove_duplicates(sample_df)

    assert len(result) == 98


def test_handle_missing_rows(sample_df):
    # Arrange: use the existing rating column.
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    # note: errors="coerce" converts invalid numeric strings to missing values.

    # Act
    result = handle_missing(df, axis="rows")

    # Assert
    assert len(result) == 97


def test_remove_outliers_iqr(sample_df):
    # Arrange: use numeric ratings and exclude missing values.
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna()
    # note: errors="coerce" converts invalid numeric strings to missing values.

    # Act
    result = remove_outliers(df, ["rating"], method="iqr", threshold=1.5)

    # Assert
    assert len(result) == 95


def test_remove_outliers_zscore(sample_df):
    # Arrange: same numeric ratings without missing values.
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna()

    # Act
    result = remove_outliers(df, ["rating"], method="zscore", threshold=3)

    # Assert: z-score also removes the two extreme ratings (200 and -50)
    assert len(result) == 95


def test_remove_outliers_with_unsupported_method(sample_df):
    # The method is checked before the data is used, so sample_df works as-is.
    with pytest.raises(ValueError, match="Unsupported outlier method"):
        remove_outliers(sample_df, ["rating"], method="unknown", threshold=1.5)