# tests/test_data_validator.py

import pytest

from src import validate_dataframe


def test_validate_dataframe_removes_invalid_ratings(sample_df):
    # Arrange
    required_columns = ["record_id", "name", "rating", "category", "status"]
    numeric_columns = ["rating"]

    # Act
    result = validate_dataframe(sample_df, required_columns, numeric_columns)

    # Assert: the 2 text ratings are gone and all five columns are still there
    assert len(result) == 98
    assert result.columns.tolist() == sample_df.columns.tolist()


def test_validate_dataframe_with_missing_column(sample_df):
    # Arrange: "price" is not a column in the sample data
    required_columns = ["record_id", "price"]
    numeric_columns = ["rating"]

    # Act + Assert
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_dataframe(sample_df, required_columns, numeric_columns)