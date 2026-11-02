import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# Shared look for every bar chart in this module.
BAR_STYLE = {
    "color": "cornflowerblue",
    "edgecolor": "navy",
    "linewidth": 1.2,
    "alpha": 0.85,
}


def main():
    sample = pd.DataFrame({
        "order_1": [0, 1, 2, np.nan, 4, 5],
        "order_2": [0, -1, np.nan, np.nan, -4, -5],
        "order_txt": ["zero", "one", "two", np.nan, "four", "five"],
    })

    plot_missing_values(sample)
    plot_correlation_matrix(sample)
    plot_categorical_distribution(sample, "order_txt")
    plot_numeric_distribution(sample, "order_1")
    plt.show()


def _style_bar_axes(ax, title, xlabel, ylabel):
    ax.set_title(title, fontsize=14, pad=12)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.tick_params(axis="x", labelrotation=30)
    ax.grid(axis="y", linestyle="--", alpha=0.35)


def plot_missing_values(df):
    """Bar chart of missing values per column.

    Returns (fig, ax), or None if no column has missing values.
    """
    result = df.isna().sum()
    result = result[result > 0]

    if result.empty:
        return None

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(result.index, result.values, width=0.65, **BAR_STYLE)
    _style_bar_axes(ax, "Missing values per column", "Columns", "Missing values count")
    fig.tight_layout()

    return fig, ax


def plot_correlation_matrix(df):
    """Heatmap of correlations between numeric columns.

    Returns (fig, ax). Raises ValueError if there are fewer than two
    numeric columns, because a correlation matrix needs a pair to compare.
    """
    corr_matrix = df.corr(numeric_only=True)

    if len(corr_matrix) < 2:
        raise ValueError("Need at least two numeric columns to correlate.")

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        vmin=-1,
        vmax=1,
        linewidths=0.5,
        square=True,
        ax=ax,
    )
    ax.set_title("Correlation Matrix Heatmap", fontsize=14, pad=12)
    fig.tight_layout()

    return fig, ax


def plot_categorical_distribution(df, column, top_n=20):
    """Bar chart of the top_n most frequent values in a column.

    Missing values are counted and shown as "Missing".
    Returns (fig, ax), or None if the column is empty.
    Raises ValueError if the column does not exist.
    """
    if column not in df.columns:
        raise ValueError(f"Column {column!r} was not found in the DataFrame.")

    counts = df[column].value_counts(dropna=False).head(top_n)
    if counts.empty:
        return None

    # Give missing values a readable label for the chart.
    counts.index = counts.index.map(
        lambda value: "Missing" if pd.isna(value) else str(value)
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(counts.index, counts.values, **BAR_STYLE)
    _style_bar_axes(ax, f"Distribution of {column} (top {top_n})", column, "Count")
    fig.tight_layout()

    return fig, ax


def plot_numeric_distribution(df, column, bins=20):
    """Histogram of a numeric column. Missing values are left out.

    Returns (fig, ax), or None if the column has no non-missing values.
    Raises ValueError if the column does not exist, TypeError if it is not numeric.
    """
    if column not in df.columns:
        raise ValueError(f"Column {column!r} was not found in the DataFrame.")
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise TypeError(f"Column {column!r} is not numeric.")

    values = df[column].dropna()
    if values.empty:
        return None

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(values, bins=bins, **BAR_STYLE)
    _style_bar_axes(ax, f"Distribution of {column}", column, "Count")
    fig.tight_layout()

    return fig, ax


if __name__ == "__main__":
    main()
