import pandas as pd

from reporting import (
    build_quality_report,
    report_to_markdown,
    save_report,
    summarize_findings,
)


def make_clean_df():
    return pd.DataFrame(
        {
            "id": ["a", "b", "c"],
            "score": [0.1, 0.5, 0.9],
            "verdict": ["YES", "NO", "UNK"],
        }
    )


def make_messy_df():
    return pd.DataFrame(
        {
            "id": ["a", "a", None, "d"],
            "score": [0.1, 1.5, -0.2, None],
            "verdict": ["YES", "maybe", "NO", "NO"],
        }
    )


def build(df):
    return build_quality_report(
        df,
        id_column="id",
        allowed_values={"verdict": ["YES", "NO", "UNK"]},
        numeric_ranges={"score": (0, 1)},
    )


def test_report_sections_without_rules():
    report = build_quality_report(make_clean_df())
    assert list(report) == ["Dataset overview", "Columns", "Missing values", "Duplicate rows"]


def test_report_sections_with_rules():
    report = build(make_clean_df())
    assert "Identifier check" in report
    assert "Categorical checks" in report
    assert "Numeric range checks" in report


def test_report_does_not_change_input():
    df = make_messy_df()
    before = df.copy()
    build(df)
    pd.testing.assert_frame_equal(df, before)


def test_numeric_range_checks_values():
    checks = build(make_messy_df())["Numeric range checks"]
    assert checks.loc["score", "below_min"] == 1
    assert checks.loc["score", "above_max"] == 1
    assert checks.loc["score", "missing"] == 1
    assert checks.loc["score", "observed_max"] == 1.5


def test_categorical_checks_values():
    checks = build(make_messy_df())["Categorical checks"]
    assert checks.loc["verdict", "unexpected_count"] == 1
    assert checks.loc["verdict", "unexpected"] == "maybe"


def test_clean_data_has_no_findings():
    assert summarize_findings(build(make_clean_df())) == []


def test_duplicate_rows_finding():
    df = pd.DataFrame({"a": [1, 1, 2, 3]})
    findings = summarize_findings(build_quality_report(df))
    assert findings == ["1 fully duplicated rows (25.0%)"]
