from pathlib import Path

import pandas as pd

from inspection import column_groups, column_overview, dataset_overview
from loading import DATA_PATH, load_data
from quality import (
    duplicate_report,
    identifier_report,
    missing_value_report,
    numerical_range_report,
    numerical_range_validator,
    validate_categorical_values,
)

REPORT_PATH = Path(__file__).resolve().parent.parent / "reports" / "quality_report.md"


def main():
    df = load_data(DATA_PATH)
    groups = column_groups(df)

    # Exploratory rules, not documented ones: YES/NO/UNK is what the verdict
    # columns contain, and [0, 1] assumes the scores and confidences are
    # probabilities. Change these if the dataset documentation says otherwise.
    verdict_columns = [column for column in df.columns if column.endswith("__verdict")]
    allowed_values = {column: ["YES", "NO", "UNK"] for column in verdict_columns}
    numeric_ranges = {column: (0, 1) for column in groups["numeric"]}

    report = build_quality_report(
        df,
        id_column="StudyInstanceUID",
        allowed_values=allowed_values,
        numeric_ranges=numeric_ranges,
    )
    text = report_to_markdown(report, title="RSNA Knee LLM Labels: data quality report")
    print(text)
    save_report(text, REPORT_PATH)
    print(f"Saved to {REPORT_PATH}")


def build_quality_report(df, id_column=None, allowed_values=None, numeric_ranges=None):
    """Run the inspection and quality checks and return {section title: DataFrame}.

    id_column: column that should hold one unique ID per row.
    allowed_values: {column: list of allowed categories}.
    numeric_ranges: {column: (min_value, max_value)}, bounds inclusive.

    Checks that need a rule only run when you pass that rule. Nothing in df is changed.
    """
    report = {
        "Dataset overview": dataset_overview(df),
        "Columns": column_overview(df),
        "Missing values": missing_value_report(df),
        "Duplicate rows": duplicate_report(df),
    }

    if id_column is not None:
        identifier = identifier_report(df, id_column)
        identifier.index = [id_column]
        report["Identifier check"] = identifier

    if allowed_values:
        rows = {}
        for column, allowed in allowed_values.items():
            unexpected = validate_categorical_values(df, column, allowed)["unexpected_value"]
            rows[column] = {
                "allowed": ", ".join(map(str, allowed)),
                "unexpected_count": len(unexpected),
                "unexpected": ", ".join(map(str, unexpected)),
            }
        report["Categorical checks"] = pd.DataFrame.from_dict(rows, orient="index")

    if numeric_ranges:
        rows = {}
        for column, (min_value, max_value) in numeric_ranges.items():
            stats = numerical_range_report(df, column)[column]
            counts = numerical_range_validator(df, column, min_value, max_value).iloc[0]
            rows[column] = {
                "allowed_min": min_value,
                "allowed_max": max_value,
                "observed_min": stats["min"],
                "observed_max": stats["max"],
                **counts.to_dict(),
            }
        report["Numeric range checks"] = pd.DataFrame.from_dict(rows, orient="index")

    return report


def summarize_findings(report):
    """Return a list of plain-English problems found in a report from build_quality_report."""
    findings = []

    missing = report["Missing values"]
    # itertuples keeps each column's dtype; iterrows would turn counts into floats
    for row in missing[missing["missing_count"] > 0].itertuples():
        findings.append(
            f"{row.Index}: {row.missing_count} missing values ({row.missing_pct}%)"
        )

    duplicates = report["Duplicate rows"]
    duplicate_count = duplicates["duplicate_count"].iloc[0]
    if duplicate_count > 0:
        findings.append(
            f"{duplicate_count} fully duplicated rows ({duplicates['duplicate_pct'].iloc[0]}%)"
        )

    if "Identifier check" in report:
        identifier = report["Identifier check"]
        id_column = identifier.index[0]
        missing_ids = identifier["missing_count"].iloc[0]
        duplicate_ids = identifier["duplicate_count"].iloc[0]
        if missing_ids > 0:
            findings.append(f"{id_column}: {missing_ids} missing IDs")
        if duplicate_ids > 0:
            findings.append(f"{id_column}: {duplicate_ids} duplicated IDs")

    if "Categorical checks" in report:
        checks = report["Categorical checks"]
        for row in checks[checks["unexpected_count"] > 0].itertuples():
            findings.append(f"{row.Index}: unexpected values {row.unexpected}")

    if "Numeric range checks" in report:
        checks = report["Numeric range checks"]
        out_of_range = checks[(checks["below_min"] > 0) | (checks["above_max"] > 0)]
        for row in out_of_range.itertuples():
            findings.append(
                f"{row.Index}: {row.below_min} values below {row.allowed_min}, "
                f"{row.above_max} above {row.allowed_max}"
            )

    return findings


def report_to_markdown(report, title="Data quality report"):
    """Render a report from build_quality_report as Markdown text."""
    findings = summarize_findings(report)

    lines = [f"# {title}", "", "## Findings", ""]
    if findings:
        lines += [f"- {finding}" for finding in findings]
    else:
        lines.append("No problems found by the checks that were run.")

    for section, table in report.items():
        lines += ["", f"## {section}", "", "```text", table.to_string(), "```"]

    return "\n".join(lines) + "\n"


def save_report(text, path):
    """Write report text to path, creating parent folders if needed. Returns the Path."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


if __name__ == "__main__":
    main()
