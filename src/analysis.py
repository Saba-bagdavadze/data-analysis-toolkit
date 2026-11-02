import pandas as pd
import numpy as np

from loading import DATA_PATH, load_data


def main():
    """Run the analysis functions on the report labels dataset."""
    df = load_data(DATA_PATH)
    print(numerical_summary(df, "Medial Meniscus"))
    print(categorical_summary(df, "Medial Meniscus__conf"))
    print(correlation_report(df, ["Medial Meniscus", "Medial Meniscus__conf"]))
    print(grouped_summary(df, "Medial Meniscus__verdict", "Medial Meniscus"))


def numerical_summary(df, column):
    """Return descriptive statistics for a given column"""
    descriptive_summary = df[column].describe()
    descriptive_frame = round(descriptive_summary.to_frame(),2)

    return descriptive_frame


def categorical_summary(df, column):
    """Return the count and percentage of each category in a column"""
    counts = df[column].value_counts(dropna=False)
    percentages = counts.div(len(df)).mul(100)

    report = {
        "count": counts,
        "percentage": percentages.round(2),
    }

    result = pd.DataFrame(report)
    return (result)
   
   
def correlation_report(df, columns=None):
    """Return the Pearson correlation matrix for numeric columns.

    If columns is None, every numeric column in df is used.

    Raises
    ------
    ValueError
        If columns is None and df has no numeric columns.
    KeyError
        If any requested column is not in df.
    TypeError
        If any requested column is not numeric.
    """
    if columns is None:
        selected = df.select_dtypes(include="number")
        if selected.empty:
            raise ValueError("No numerical columns are available.")
    else:
        if isinstance(columns, str):
            columns = [columns]

        missing = []

        for column in columns:
            if column not in df.columns:
                missing.append(column)

        if missing:
            raise KeyError(f"Columns not found: {missing}")


        non_numeric = []

        for column in columns:
            if column in df.columns and not pd.api.types.is_numeric_dtype(df[column]):
                non_numeric.append(column)

        if non_numeric:
            raise TypeError(f"Columns are not numeric: {non_numeric}")

        selected = df[columns]

    return selected.corr(method="pearson")

   
def grouped_summary(df, group_column, value_column):
    """Return descriptive statistics of a column for each group"""
    summary = df.groupby(group_column)[value_column].describe()
    return summary


if __name__ == "__main__":
    main()
