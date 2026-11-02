import pandas as pd
import pytest

from quality import (
    duplicate_report,
    identifier_report,
    missing_value_report,
    numerical_range_report,
    numerical_range_validator,
    validate_categorical_values,
)


def make_people_df():
    return pd.DataFrame(
        {
            "Name": ["Saba", "Nita", "Levan"],
            "Age": [24, None, 24],
            "City": ["Tbilisi", None, None],
        },
        index=["person 1", "person 2", "person 3"],
    )


def make_id_df():
    return pd.DataFrame({"ID": ["A", "B", None, None, "B"]})


def test_missing_value_report():
    result = missing_value_report(make_people_df())
    assert result.loc["Name", "missing_count"] == 0
    assert result.loc["Age", "missing_count"] == 1
    assert result.loc["City", "missing_count"] == 2
    assert result.loc["City", "missing_pct"] == 66.67


def test_duplicate_report():
    df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})
    result = duplicate_report(df)
    assert result["duplicate_count"].iloc[0] == 1
    assert result["duplicate_pct"].iloc[0] == 33.33


def test_duplicate_report_empty_raises():
    with pytest.raises(ValueError):
        duplicate_report(pd.DataFrame({"a": []}))


def test_identifier_report_ignores_missing_ids():
    result = identifier_report(make_id_df(), "ID")
    assert result["missing_count"].iloc[0] == 2
    assert result["duplicate_count"].iloc[0] == 1
    assert result["duplicate_pct"].iloc[0] == 20.0


def test_validate_categorical_values():
    df = pd.DataFrame({"verdict": ["YES", "maybe", None, "NO", "??", "maybe"]})
    result = validate_categorical_values(df, "verdict", ["YES", "NO", "UNK"])
    assert list(result["unexpected_value"]) == ["??", "maybe"]


def test_numerical_range_validator():
    df = pd.DataFrame({"x": [0.1, 0.2, 0.5, 0.7, 0.9, None]})
    result = numerical_range_validator(df, "x", 0.2, 0.7)
    assert result["below_min"].iloc[0] == 1
    assert result["above_max"].iloc[0] == 1
    assert result["missing"].iloc[0] == 1


def test_numerical_range_report():
    df = pd.DataFrame({"x": [0.1, 0.5, 0.9, None]})
    result = numerical_range_report(df, "x")
    assert list(result.index) == ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]
    assert result.loc["count", "x"] == 3
    assert result.loc["min", "x"] == 0.1
    assert result.loc["max", "x"] == 0.9
    assert result.loc["mean", "x"] == pytest.approx(0.5)


def test_numerical_range_report_non_numeric_raises():
    df = pd.DataFrame({"verdict": ["YES", "NO"]})
    with pytest.raises(TypeError, match="not numeric"):
        numerical_range_report(df, "verdict")
