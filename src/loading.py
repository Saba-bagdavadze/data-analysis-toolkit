from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "report_labels_v2.csv"


def _read_tsv(path, **kwargs):
    return pd.read_csv(path, sep="\t", **kwargs)


# File extension -> pandas reader. Excel needs openpyxl, parquet needs pyarrow.
READERS = {
    ".csv": pd.read_csv,
    ".tsv": _read_tsv,
    ".xlsx": pd.read_excel,
    ".xls": pd.read_excel,
    ".json": pd.read_json,
    ".parquet": pd.read_parquet,
}


def main():
    df = load_data(DATA_PATH)
    print(df.head())


def load_data(path, **kwargs):
    """Load a tabular file into a DataFrame, choosing the reader from the file extension.

    Extra keyword arguments are passed to the pandas reader (e.g. usecols, nrows).
    Raises FileNotFoundError if the file does not exist and ValueError if the
    extension is not supported.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"No file found at {path}")

    reader = READERS.get(path.suffix.lower())
    if reader is None:
        raise ValueError(
            f"Unsupported file type '{path.suffix}'. Supported: {sorted(READERS)}"
        )

    result = reader(path, **kwargs)
    return result


if __name__ == "__main__":
    main()
