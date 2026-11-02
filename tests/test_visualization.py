import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from visualization import (
    plot_categorical_distribution,
    plot_correlation_matrix,
    plot_missing_values,
    plot_numeric_distribution,
)


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


def make_orders_df():
    return pd.DataFrame(
        {
            "order_1": [0, 1, 2, np.nan, 4, 5],
            "order_2": [0, -1, np.nan, np.nan, -4, -5],
            "order_txt": ["zero", "one", "two", np.nan, "four", "five"],
            "complete": [1, 2, 3, 4, 5, 6],
        }
    )


def bar_heights(ax):
    return [patch.get_height() for patch in ax.patches]


def tick_labels(ax):
    return [label.get_text() for label in ax.get_xticklabels()]


def test_plot_missing_values():
    fig, ax = plot_missing_values(make_orders_df())
    assert tick_labels(ax) == ["order_1", "order_2", "order_txt"]
    assert bar_heights(ax) == [1, 2, 1]
    assert ax.get_title() == "Missing values per column"


def test_plot_missing_values_no_missing():
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    assert plot_missing_values(df) is None


def test_plot_correlation_matrix():
    fig, ax = plot_correlation_matrix(make_orders_df())
    values = ax.collections[0].get_array().reshape(3, 3)
    assert np.allclose(np.diag(values), 1.0)
    assert values[0, 1] == pytest.approx(-1.0)


def test_plot_correlation_matrix_ignores_text_columns():
    fig, ax = plot_correlation_matrix(make_orders_df())
    labels = [label.get_text() for label in ax.get_xticklabels()]
    assert "order_txt" not in labels


def test_plot_correlation_matrix_too_few_numeric_columns():
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    with pytest.raises(ValueError):
        plot_correlation_matrix(df)


def test_plot_categorical_distribution():
    df = pd.DataFrame({"city": ["Tbilisi", "Batumi", "Tbilisi", np.nan]})
    fig, ax = plot_categorical_distribution(df, "city")
    assert tick_labels(ax) == ["Tbilisi", "Batumi", "Missing"]
    assert bar_heights(ax) == [2, 1, 1]


def test_plot_categorical_distribution_top_n():
    df = pd.DataFrame({"letter": list("aaabbc")})
    fig, ax = plot_categorical_distribution(df, "letter", top_n=2)
    assert tick_labels(ax) == ["a", "b"]
    assert "top 2" in ax.get_title()


def test_plot_categorical_distribution_missing_column():
    with pytest.raises(ValueError):
        plot_categorical_distribution(make_orders_df(), "not_a_column")


def test_plot_categorical_distribution_empty_column():
    df = pd.DataFrame({"city": pd.Series([], dtype=object)})
    assert plot_categorical_distribution(df, "city") is None


def test_plot_numeric_distribution():
    fig, ax = plot_numeric_distribution(make_orders_df(), "order_1", bins=5)
    assert sum(bar_heights(ax)) == 5
    assert len(ax.patches) == 5
    assert ax.get_title() == "Distribution of order_1"


def test_plot_numeric_distribution_missing_column():
    with pytest.raises(ValueError):
        plot_numeric_distribution(make_orders_df(), "not_a_column")


def test_plot_numeric_distribution_text_column():
    with pytest.raises(TypeError):
        plot_numeric_distribution(make_orders_df(), "order_txt")


def test_plot_numeric_distribution_all_missing():
    df = pd.DataFrame({"x": [np.nan, np.nan]})
    assert plot_numeric_distribution(df, "x") is None
