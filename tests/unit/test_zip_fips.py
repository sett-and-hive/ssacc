"""Test ZipFips."""
from pathlib import Path

from ssacc.zip_fips import ZipFips


def test_construction():
    """Test construction of ZipFips. Trivial."""
    assert ZipFips()


def test_read_csv():
    """Test read_csv() on the happy path."""
    project_root = Path(__file__).parents[1]
    file_path = project_root.joinpath("data", "test1.csv")
    print(file_path)
    required_columns = {"ssacounty", "rating", "year", "runtime"}
    df = ZipFips.read_csv(file_path)
    assert len(df)
    for column_name in required_columns:
        assert column_name in df.columns


def test_read_csv_file_not_found():
    """Test read_csv() for bad path."""
    project_root = Path(__file__).parents[1]
    file_path = project_root.joinpath("data", "file_not_found.csv")
    print(file_path)
    df = ZipFips.read_csv(file_path)
    assert df is None


def test_read_csv_exception():
    """Test read_csv() for bad data frame."""
    project_root = Path(__file__).parents[1]
    file_path = project_root.joinpath("data", "test1.csv")
    print(file_path)
    df = ZipFips.read_csv(None)
    assert df is None
