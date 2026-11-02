import pandas as pd
import pytest

from loading import load_data


def test_load_csv(tmp_path):
    path = tmp_path / "people.csv"
    path.write_text("name,age\nSaba,24\nNita,30\n")
    result = load_data(path)
    assert list(result.columns) == ["name", "age"]
    assert len(result) == 2
    assert result.loc[0, "name"] == "Saba"


def test_load_tsv(tmp_path):
    path = tmp_path / "people.tsv"
    path.write_text("name\tage\nSaba\t24\n")
    result = load_data(path)
    assert list(result.columns) == ["name", "age"]


def test_load_passes_kwargs(tmp_path):
    path = tmp_path / "people.csv"
    path.write_text("name,age\nSaba,24\nNita,30\n")
    result = load_data(path, usecols=["age"], nrows=1)
    assert list(result.columns) == ["age"]
    assert len(result) == 1


def test_load_accepts_string_path(tmp_path):
    path = tmp_path / "people.csv"
    path.write_text("name\nSaba\n")
    assert isinstance(load_data(str(path)), pd.DataFrame)


def test_load_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_data(tmp_path / "nope.csv")


def test_load_unsupported_extension_raises(tmp_path):
    path = tmp_path / "notes.txt"
    path.write_text("hello")
    with pytest.raises(ValueError, match="Unsupported file type"):
        load_data(path)
