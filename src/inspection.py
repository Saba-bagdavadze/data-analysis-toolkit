import pandas as pd

from loading import DATA_PATH, load_data


def main():
    df = load_data(DATA_PATH)

    print(dataset_overview(df))
    print(column_overview(df))
    print(column_groups(df))


def dataset_overview(df):
    """Return the number of rows, number of columns and memory use (MB) of the DataFrame."""
    memory_mb = df.memory_usage(deep=True).sum() / 1024**2

    report = {
        "rows": [df.shape[0]],
        "columns": [df.shape[1]],
        "memory_mb": [round(memory_mb, 2)],
    }
    result = pd.DataFrame(report)
    return result


def _first_value(column):
    """Return the first non-missing value in a Series, or None if there is none."""
    values = column.dropna()
    if values.empty:
        return None
    return values.iloc[0]


def column_overview(df):
    """Return dtype, non-missing count, unique count and an example value for each column.

    Missing values are not counted as a unique value; missing_value_report covers them.
    """
    report = {
        "dtype": df.dtypes.astype(str),
        "non_null_count": df.notna().sum(),
        "unique_count": df.nunique(),
        "example": pd.Series({column: _first_value(df[column]) for column in df.columns}),
    }
    result = pd.DataFrame(report)
    return result


def column_groups(df):
    """Split column names into 'numeric', 'datetime' and 'categorical' (everything else).

    Booleans count as categorical.
    """
    numeric = list(df.select_dtypes(include="number", exclude="bool").columns)
    datetime = list(df.select_dtypes(include="datetime").columns)
    categorical = [column for column in df.columns if column not in numeric + datetime]

    return {
        "numeric": numeric,
        "datetime": datetime,
        "categorical": categorical,
    }


if __name__ == "__main__":
    main()
