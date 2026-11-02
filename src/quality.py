from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "report_labels_v2.csv"


def main():
    df = pd.read_csv(DATA_PATH)

    print(missing_value_report(df))
    print(duplicate_report(df))
    print(identifier_report(df, "StudyInstanceUID"))
    print(categorical_value_report(df, "ACL__verdict"))
    print(validate_categorical_values(df, "ACL__verdict", ["YES", "NO", "UNK"]))
    print(numerical_range_report(df, "ACL"))
    print(numerical_range_validator(df, "ACL", 0.2, 0.7))


def _percent(count, total):
    """Return count as a percentage of total, rounded to 2 decimals."""
    if total == 0:
        raise ValueError("Cannot compute a percentage of an empty DataFrame")
    return round(count / total * 100, 2)


def missing_value_report(df):
    """Return missing-value counts and percentages for each column."""
    missing_count = df.isna().sum()
    total_rows = df.shape[0]

    report = {
        "missing_count": missing_count,
        "missing_pct": _percent(missing_count, total_rows),
    }
    result = pd.DataFrame(report)
    return result


def duplicate_report(df):
    """Return the count and percentage of fully duplicated rows in the DataFrame."""
    duplicate_count = df.duplicated().sum()
    total_rows = df.shape[0]

    report = {
        "duplicate_count": [duplicate_count],
        "duplicate_pct": [_percent(duplicate_count, total_rows)],
    }
    result = pd.DataFrame(report)
    return result


def identifier_report(df, column):
    """Return missing count, duplicate count and duplicate percentage for an ID column.

    Missing IDs are not counted as duplicates. The percentage is out of all rows.
    """
    missing_count = df[column].isna().sum()
    duplicate_count = df[column].dropna().duplicated().sum()
    total_rows = df.shape[0]

    report = {
        "missing_count": [missing_count],
        "duplicate_count": [duplicate_count],
        "duplicate_pct": [_percent(duplicate_count, total_rows)],
    }
    result = pd.DataFrame(report)
    return result


def categorical_value_report(df, column):
    """Return the count of each value in a column, including missing values."""
    values_count = df[column].value_counts(dropna=False)

    report = {
        "count": values_count,
    }
    result = pd.DataFrame(report)
    return result


def validate_categorical_values(df, column, allowed_values):
    """Return the sorted values in a column that are not in allowed_values.

    Missing values are ignored here; missing_value_report covers them.
    """
    unique_values = set(df[column].dropna().unique())
    unexpected_values = sorted(unique_values.difference(allowed_values))

    report = {
        "unexpected_value": unexpected_values,
    }
    result = pd.DataFrame(report)
    return result


def numerical_range_report(df, column):
    """Return descriptive statistics (count, mean, std, min, quartiles, max) for a numeric column.

    Missing values are left out of the statistics; missing_value_report covers them.
    """
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise TypeError(f"Column '{column}' is not numeric")

    result = df[column].describe().to_frame()
    return result


def numerical_range_validator(df, column, min_value, max_value):
    """Return the number of values below min_value, above max_value, and missing.

    Bounds are inclusive: a value equal to min_value or max_value is in range.
    """
    below_count = (df[column] < min_value).sum()
    above_count = (df[column] > max_value).sum()
    missing_count = df[column].isna().sum()

    report = {
        "below_min": [below_count],
        "above_max": [above_count],
        "missing": [missing_count],
    }
    result = pd.DataFrame(report)
    return result


if __name__ == "__main__":
    main()
