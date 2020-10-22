"""Test ZipFips."""
import json
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
    assert not df.empty
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


def test_read_zip_fips_text_file():
    """Test read_zip_fips_text_file with happy path input file"""
    project_root = Path(__file__).resolve().parents[2]
    state_file = project_root.joinpath("data", "source", "state_fips.json")
    statecodes = json.load(open(state_file))
    test_file = project_root.joinpath("tests", "data", "zipcty-fake.txt")
    df = ZipFips.read_zip_fips_text_file(test_file, statecodes)
    assert not df.empty
    assert "AK" in df.statecd.values


def test_read_zip_fips_text_file_too_short():
    """Test read_zip_fips_text_file with header but no content input file"""
    project_root = Path(__file__).resolve().parents[2]
    state_file = project_root.joinpath("data", "source", "state_fips.json")
    statecodes = json.load(open(state_file))
    test_file = project_root.joinpath("tests", "data", "zipcty-too-short.txt")
    df = ZipFips.read_zip_fips_text_file(test_file, statecodes)
    assert df.empty


def test_read_zip_fips_text_file_bad_state():
    """
    Test read_zip_fips_text_file with input file with a bad state code
    which leads to 00 as fips state code
    """
    project_root = Path(__file__).resolve().parents[2]
    state_file = project_root.joinpath("data", "source", "state_fips.json")
    statecodes = json.load(open(state_file))
    test_file = project_root.joinpath("tests", "data", "zipcty-fake-state.txt")
    df = ZipFips.read_zip_fips_text_file(test_file, statecodes)
    assert not df.empty
    assert "00" in str(df.fipsstct.values)


def test_read_zip_fips_text_file_bad_content():
    """Test read_zip_fips_text_file with content line that won't match RE"""
    project_root = Path(__file__).resolve().parents[2]
    state_file = project_root.joinpath("data", "source", "state_fips.json")
    statecodes = json.load(open(state_file))
    test_file = project_root.joinpath("tests", "data", "zipcty-bad-data.txt")
    df = ZipFips.read_zip_fips_text_file(test_file, statecodes)
    assert df.empty


def test_read_zip_fips_text_file_repeat_zip_code():
    """Test read_zip_fips_text_file with repeated ZIP code"""
    project_root = Path(__file__).resolve().parents[2]
    state_file = project_root.joinpath("data", "source", "state_fips.json")
    statecodes = json.load(open(state_file))
    test_file = project_root.joinpath("tests", "data", "zipcty-test.txt")
    df = ZipFips.read_zip_fips_text_file(test_file, statecodes)
    assert not df.empty
    assert "TX" in df.statecd.values


def test_files_to_csv():
    """Test files_to_csv with test files"""
    project_root = Path(__file__).resolve().parents[2]
    test_file_path = project_root.joinpath("tests", "data")
    df = ZipFips.files_to_csv(test_file_path)
    assert not df.empty
    assert "TX" in df.statecd.values
