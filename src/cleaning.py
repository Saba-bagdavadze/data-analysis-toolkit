import pandas as pd
import numpy as np


def handle_missing_values(df, column, strategy, value=None):
    """Fill or drop missing values in one column. strategy is 'fill' or 'drop'."""
    result = df.copy()
    if strategy == "fill":
        if value is None:
            raise ValueError("strategy='fill' requires a value")
        result[column] = result[column].fillna(value)
    elif strategy == "drop":
        result = result.dropna(subset=[column])
    else:
        raise ValueError("The strategy must be 'fill' or 'drop'")
    return result


def remove_duplicates(df, subset=None, keep="first"):
    """Return df without duplicate rows (optionally judged on subset columns)."""
    return df.drop_duplicates(subset=subset, keep=keep)


def convert_column_types(df, column, dtype):
    """Convert a column to dtype. For int/float, unparseable values become NaN."""
    result = df.copy()
    if dtype in (int, "int"):
        # Nullable Int64 can hold NaN; plain int can't
        result[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")
    elif dtype in (float, "float"):
        result[column] = pd.to_numeric(df[column], errors="coerce")
    else:
        result[column] = df[column].astype(dtype)
    return result


def standardize_categories(df, column):
    """Strip whitespace and uppercase a text column."""
    result = df.copy()
    try:
        result[column] = df[column].str.strip().str.upper()
    except AttributeError as err:
        raise TypeError(f"Column '{column}' is not a text column") from err
    return result


if __name__ == "__main__":
    data = {
        'School ID': [101, 102, "Uknown", 107, 105, 106, 107, 108],
        'Name': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
        'Address': ['123 Main St', '456 Oak Ave', '789 Pine Ln', '101 Elm St', np.nan, '222 Maple Rd', '444 Cedar Blvd', '555 Birch Dr'],
        'City': ['Mumbai', 'Delhi', 'Bengaluru', 'Chennai', 'Kolkata', np.nan, 'Pune', 'Jaipur'],
        'Subject': ['Math', 'English', 'Science', 'Math', 'History', 'Math', 'Science', 'English'],
        'Marks': [85, 92, 78, 89, np.nan, 95, 80, 88],
        'Rank': [2, 1, 4, 3, 8, 1, 5, 3],
        'Grade': ['B', 'A', 'C', 'B', 'D', 'A', 'C', 'B']
    }
    df = pd.DataFrame(data)

    print(standardize_categories(df, "Subject"))
    print(convert_column_types(df, "School ID", int)["School ID"])
    print(remove_duplicates(df, subset=["School ID"], keep="last"))
    print(handle_missing_values(df, "Marks", "fill", value=0))
