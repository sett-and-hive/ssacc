"""Test CSV utils for adapters."""

import pytest

from ssacc.adapters import csv_utils
from ssacc.utils import utils


def test_create_dataframe_from_csv():
    """Happy path test for CSV read util."""
    project_root = utils.get_project_root()
    file_path = project_root.joinpath("tests", "data", "test1.csv")
    df = csv_utils.create_dataframe_from_csv(file_path)
    assert not df.empty


def test_create_dataframe_from_missing_csv():
    """Missing filepath test for CSV read util."""
    project_root = utils.get_project_root()
    file_path = project_root.joinpath("tests", "data", "missing.csv")
    df = csv_utils.create_dataframe_from_csv(file_path)
    assert df is None


def test_create_dataframe_from_bad_csv():
    """Test for malformed CSV read util."""
    project_root = utils.get_project_root()
    file_path = project_root.joinpath("tests", "data", "parse-error.csv")
    df = csv_utils.create_dataframe_from_csv(file_path)
    assert df is None


def test_create_dataframe_from_empty_csv():
    """Test for empty CSV read util."""
    with pytest.raises(Exception):
        project_root = utils.get_project_root()
        file_path = project_root.joinpath("tests", "data", "empty.csv")
        df = csv_utils.create_dataframe_from_csv(file_path)
        assert df is None
