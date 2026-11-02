# Exploratory Data Analysis Toolkit

A small, reusable Python toolkit for exploring tabular data and checking its quality, built with pandas.
It was developed against the [RSNA Knee LLM Labels](https://www.kaggle.com/) dataset (`data/report_labels_v2.csv`), but every function takes a plain DataFrame and works on any dataset.

Checking and cleaning are kept separate. `quality.py` and `reporting.py` only report problems and never change your data. Cleaning happens only when you ask for it: every function in `cleaning.py` takes the strategy you choose and returns a new DataFrame, leaving your input untouched.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Modules

| Module | What it does | Functions |
|---|---|---|
| `loading.py` | Load a file into a DataFrame, picking the reader from the extension (csv, tsv, xlsx, json, parquet) | `load_data` |
| `inspection.py` | First look at the data's structure | `dataset_overview`, `column_overview`, `column_groups` |
| `quality.py` | Report and validate data quality | `missing_value_report`, `duplicate_report`, `identifier_report`, `categorical_value_report`, `validate_categorical_values`, `numerical_range_report`, `numerical_range_validator` |
| `cleaning.py` | Clean data with an explicit strategy | `handle_missing_values`, `remove_duplicates`, `convert_column_types`, `standardize_categories` |
| `analysis.py` | Summaries and relationships | `numerical_summary`, `categorical_summary`, `correlation_report`, `grouped_summary` |
| `visualization.py` | Plots. Each returns `(fig, ax)` | `plot_missing_values`, `plot_correlation_matrix`, `plot_categorical_distribution`, `plot_numeric_distribution` |
| `reporting.py` | Combine checks into one Markdown report | `build_quality_report`, `summarize_findings`, `report_to_markdown`, `save_report` |

## Workflow

Using the toolkit is a lot like checking a spreadsheet before you trust it. There are five steps:

1. Open the file. `load_data` reads it into a table.
2. Look at it. `dataset_overview` and `column_overview` tell you how big the table is and what each column holds.
3. Check it for problems. `build_quality_report` looks for empty cells, repeated rows and values that don't belong, and tells you what it found without changing anything.
4. Fix what's wrong. The functions in `cleaning.py` fix one problem at a time, and only the ones you choose. Then run step 3 again to confirm everything is fixed.
5. Explore. Use `analysis.py` for summaries and `visualization.py` for charts.

Steps 1 to 3 in code (run from the project root):

```python
import sys; sys.path.insert(0, "src")

from loading import load_data
from inspection import dataset_overview
from reporting import build_quality_report, summarize_findings

df = load_data("data/report_labels_v2.csv")   # 1. open the file
print(dataset_overview(df))                   # 2. look at it

report = build_quality_report(df, id_column="StudyInstanceUID")   # 3. check it
print(summarize_findings(report))             # a list of problems, or [] if there are none
```

To also check that a column only has certain values, or that numbers stay in a range, give the report those rules:

```python
report = build_quality_report(
    df,
    id_column="StudyInstanceUID",
    allowed_values={"ACL__verdict": ["YES", "NO", "UNK"]},   # only these words are allowed
    numeric_ranges={"ACL": (0, 1)},                          # numbers must be between 0 and 1
)
```

### Scripts and demos

Run the full report on the knee dataset:

```bash
python src/reporting.py        # prints the report and writes reports/quality_report.md
```

Each module also has a `main()` demo, for example `python src/quality.py`.

## Validation rules are assumptions

The rules in `reporting.main()` come from exploring the data, not from the dataset's documentation:

- verdict columns may only contain `YES`, `NO` or `UNK`, because those are the only values seen
- score and `__conf` columns must lie in `[0, 1]`, on the assumption that they are probabilities

Pass different rules to `build_quality_report` if the documentation says otherwise.

## Tests

```bash
pytest
```

`pytest.ini` puts `src/` on the import path, so the tests import modules directly (`from quality import ...`).
