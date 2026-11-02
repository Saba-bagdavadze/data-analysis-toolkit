import numpy as np
import pandas as pd

from inspection import column_groups, column_overview, dataset_overview


def make_mixed_df():
    return pd.DataFrame(
        {
            "score": [0.1, np.nan, 0.1],
            "verdict": [np.nan, "NO", "YES"],
            "flag": [True, False, True],
            "date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
            "empty": [np.nan, np.nan, np.nan],
        }
    )


def test_dataset_overview():
    result = dataset_overview(make_mixed_df())
    assert result["rows"].iloc[0] == 3
    assert result["columns"].iloc[0] == 5
    assert result["memory_mb"].iloc[0] >= 0


def test_column_overview_counts():
    result = column_overview(make_mixed_df())
    assert list(result.index) == ["score", "verdict", "flag", "date", "empty"]
    assert result.loc["score", "non_null_count"] == 2
    assert result.loc["score", "unique_count"] == 1
    assert result.loc["verdict", "unique_count"] == 2


def test_column_overview_example_skips_missing():
    result = column_overview(make_mixed_df())
    assert result.loc["verdict", "example"] == "NO"
    assert result.loc["score", "example"] == 0.1
    assert result.loc["empty", "example"] is None


def test_column_groups():
    result = column_groups(make_mixed_df())
    assert result["numeric"] == ["score", "empty"]
    assert result["datetime"] == ["date"]
    assert result["categorical"] == ["verdict", "flag"]
