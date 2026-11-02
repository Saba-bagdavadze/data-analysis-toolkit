import pandas as pd
import pytest
import numpy as np

from cleaning import (
    handle_missing_values,
    remove_duplicates,
    convert_column_types,
    standardize_categories,
)


def make_example_df():
    return pd.DataFrame(
        {
            'School ID': [101, 102, np.nan, 107, 105, 106, 107, 108],
            'Name': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
            'Address': ["123" , "456" , "789", "101" , "44", "222", "444" , "555"],
            'City': ['Mumbai', 'Delhi', 'Bengaluru', 'Chennai', 'Kolkata', np.nan, 'Pune', 'Jaipur'],
            'Subject': ['Math', 'English', 'Science', 'Math', 'History', 'Math', 'Science', 'English'],
            'Marks': [85, 92, 78, 89, np.nan, 95, 80, 88],
            'Rank': [2, 1, 4, 3, "uknown", 1, 5, 3],
            'Grade': ['B', 'A', 'C', 'B', 'D', 'A', 'C', 'B']

        }
    )


def make_cars_df():
    return pd.DataFrame({"cars" : ["porsche", "porsche", "mercedes", "BMW", "mercedes","porsche"]})


def test_fill_missing_values():
    result = handle_missing_values(make_example_df(),"School ID", "fill", 0)
    assert not result["School ID"].isna().any()
    assert result["School ID"].iloc[2] == 0
    assert result["School ID"].iloc[0] == 101


def test_drop_missing_values():
    result = handle_missing_values(make_example_df(),"School ID", "drop")
    assert len(result) == 7
    assert not result["School ID"].isna().any()
    assert "C" not in list(result["Name"])


def test_invalid_strategy():
    with pytest.raises(ValueError, match="'fill' or 'drop'"):
        handle_missing_values(make_example_df(),"School ID", "delete", 0)


def test_fill_without_value():
    with pytest.raises(ValueError, match="requires a value"):
        handle_missing_values(make_example_df(),"School ID", "fill", None)


def test_drop_duplicates():
    result = remove_duplicates(make_cars_df())
    assert list(result["cars"]) == ["porsche", "mercedes", "BMW"]


def test_drop_duplicates_keep_last():
    result = remove_duplicates(make_cars_df(), keep="last")
    assert list(result["cars"]) == ["BMW", "mercedes", "porsche"]
    assert list(result.index) == [3, 4, 5]


def test_drop_duplicates_subset():
    df = pd.DataFrame({"cars": ["porsche", "porsche", "BMW"], "color": ["red", "blue", "red"]})
    assert len(remove_duplicates(df)) == 3
    assert len(remove_duplicates(df, subset=["cars"])) == 2


def test_convert_int_invalid_set_NaN():
    result = convert_column_types(make_example_df(),"Rank",int)
    assert result["Rank"].isna().iloc[4]
    assert result["Rank"].dtype == "Int64"


def test_convert_flt_invalid_set_NaN():
    result = convert_column_types(make_example_df(),"Rank",float)
    assert result["Rank"].isna().iloc[4]
    assert result["Rank"].dtype == "float64"


def test_convert_type():
    df = pd.DataFrame({"score": ["12", "UFO"]})
    result = convert_column_types(df,"score",int)
    assert result["score"].iloc[0] == 12
    assert result["score"].isna().iloc[1]
    assert df["score"].iloc[0] == "12"


def test_convert_other_type():
    df = pd.DataFrame({"code": [1, 2]})
    result = convert_column_types(df, "code", str)
    assert list(result["code"]) == ["1", "2"]


def test_standardize_categories():
    df = pd.DataFrame({"Name" : ["Rob", " bob ", " Ron"]})
    result = standardize_categories(df, "Name")
    assert result["Name"].iloc[0] == "ROB"
    assert result["Name"].iloc[1] == "BOB"
    assert result["Name"].iloc[2] == "RON"


def test_standardize_non_text_column():
    with pytest.raises(TypeError, match="not a text column"):
        standardize_categories(make_example_df(), "Marks")
