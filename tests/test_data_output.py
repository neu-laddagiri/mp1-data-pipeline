# tests/test_data_output.py

import pandas as pd

from src import save_data


def test_save_data_creates_csv(sample_df, tmp_path):
    output_path = tmp_path / "clean.csv"

    # Act
    result = save_data(sample_df, output_path)

    # Assert: it saved where we asked, with the same rows and columns
    assert result == output_path
    saved = pd.read_csv(result)
    assert len(saved) == len(sample_df)
    assert saved.columns.tolist() == sample_df.columns.tolist()