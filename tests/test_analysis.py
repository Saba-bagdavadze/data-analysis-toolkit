import pandas as pd
import pytest
import numpy as np 

from analysis import (
    numerical_summary,
    categorical_summary,
    correlation_report,
    grouped_summary,
)


def make_sample_df():
    return pd.DataFrame({
        "order_1" : [0, 1, 2, 3, 4, 5],
        "order_2" : [0, -1, -2, -3, -4, -5],
        "order_txt": ["zero", "one", "two", np.nan, "four", "five"],
    })

def test_framing_summary():
    indices = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
    result = numerical_summary(make_sample_df(), "order_1")
    assert list(result.index) == indices
    assert result.columns[0] == 'order_1'

def test_frame_values():
    result = numerical_summary(make_sample_df(), "order_1")
    assert result.loc["count", "order_1"] == 6.0
    assert result.loc["min","order_1"] == 0
    assert result.loc["max","order_1"] == 5.0
    assert result.loc["mean","order_1"] == 2.5
    assert result.loc["std","order_1"] == pytest.approx(1.87)

def test_categorical_count_summary():
    result = categorical_summary(make_sample_df(), "order_txt")
    assert result.shape[0] == 6
    assert result.loc["zero","count"] == 1
    assert result.loc[np.nan,"count"] == 1
    assert result.loc["one","count"] == 1


def test_categorical_perc_summary():
    result = categorical_summary(make_sample_df(), "order_txt")
    assert result.loc["zero", "percentage"] == 16.67
    assert result.loc["one", "percentage"] == 16.67
    assert result.loc["two", "percentage"] == 16.67
    assert result.loc[np.nan, "percentage"] == 16.67


def test_categorical_totals():
    df = make_sample_df()
    result = categorical_summary(df, "order_txt")
    assert result["count"].sum() == len(df)
    assert result["percentage"].sum() == pytest.approx(100, abs=0.1)


def test_categorical_counts_repeated_values():
    df = pd.DataFrame({"colour": ["red", "red", "blue", "red"]})
    result = categorical_summary(df, "colour")
    assert result.index[0] == "red"
    assert result.loc["red", "count"] == 3
    assert result.loc["red", "percentage"] == 75.0
    assert result.loc["blue", "percentage"] == 25.0


def test_correlation_defaults_to_numeric_columns():
    result = correlation_report(make_sample_df())
    assert list(result.index) == ["order_1", "order_2"]
    assert list(result.columns) == ["order_1", "order_2"]
    assert "order_txt" not in result.columns


def test_correlation_values():
    result = correlation_report(make_sample_df())
    assert result.loc["order_1", "order_1"] == pytest.approx(1.0)
    assert result.loc["order_1", "order_2"] == pytest.approx(-1.0)
    assert result.loc["order_2", "order_1"] == pytest.approx(-1.0)


def test_correlation_selected_columns():
    df = make_sample_df()
    df["order_3"] = [5, 3, 4, 1, 2, 0]
    result = correlation_report(df, ["order_1", "order_3"])
    assert list(result.columns) == ["order_1", "order_3"]
    assert "order_2" not in result.columns


def test_correlation_accepts_single_column_name():
    result = correlation_report(make_sample_df(), "order_1")
    assert result.shape == (1, 1)
    assert result.loc["order_1", "order_1"] == pytest.approx(1.0)


def test_correlation_missing_column_raises():
    with pytest.raises(KeyError, match="order_99"):
        correlation_report(make_sample_df(), ["order_1", "order_99"])


def test_correlation_non_numeric_column_raises():
    with pytest.raises(TypeError, match="order_txt"):
        correlation_report(make_sample_df(), ["order_1", "order_txt"])


def test_correlation_missing_checked_before_non_numeric():
    with pytest.raises(KeyError):
        correlation_report(make_sample_df(), ["order_txt", "order_99"])


def test_correlation_no_numeric_columns_raises():
    df = pd.DataFrame({"name": ["a", "b", "c"]})
    with pytest.raises(ValueError, match="No numerical columns"):
        correlation_report(df)


def make_grouped_df():
    return pd.DataFrame({
        "group": ["a", "a", "b"],
        "value": [1, 3, 5],
    })


def test_grouped_summary_shape():
    result = grouped_summary(make_grouped_df(), "group", "value")
    assert list(result.index) == ["a", "b"]
    assert list(result.columns) == ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]


def test_grouped_summary_values():
    result = grouped_summary(make_grouped_df(), "group", "value")
    assert result.loc["a", "count"] == 2
    assert result.loc["a", "mean"] == 2.0
    assert result.loc["a", "min"] == 1
    assert result.loc["a", "max"] == 3
    assert result.loc["b", "mean"] == 5.0


def test_grouped_summary_single_row_group_has_nan_std():
    result = grouped_summary(make_grouped_df(), "group", "value")
    assert pd.isna(result.loc["b", "std"])
