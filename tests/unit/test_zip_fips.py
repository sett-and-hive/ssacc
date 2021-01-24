"""Test ZipFips."""


import warnings

from ssacc.utils import utils

# suppress spurious "numpy.ufunc size changed" warnings
# According to
# https://stackoverflow.com/questions/40845304/runtimewarning-numpy-dtype-size-changed-may-indicate-binary-incompatibility
# these warnings are benign.
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", message="numpy.dtype size changed")
    warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
    from ssacc.zip_fips import ZipFips

# Tests do not need to be DRY
# pylint: disable=duplicate-code
# pylint: disable=R0801


def test_construction():
    """Test construction of ZipFips. Trivial."""
    assert ZipFips()


def test_read_csv():
    """Test read_csv() on the happy path."""
    project_root = utils.get_project_root()
    file_path = project_root.joinpath("tests", "data", "test1.csv")
    print(file_path)
    required_columns = {"ssacounty", "rating", "year", "runtime"}
    df = ZipFips.read_csv(file_path)
    assert not df.empty
    for column_name in required_columns:
        assert column_name in df.columns


def test_read_csv_file_not_found():
    """Test read_csv() for bad path."""
    project_root = utils.get_project_root()
    file_path = project_root.joinpath("tests", "data", "file_not_found.csv")
    print(file_path)
    df = ZipFips.read_csv(file_path)
    assert df is None


def test_read_csv_exception():
    """Test read_csv() for bad data frame."""
    project_root = utils.get_project_root()
    file_path = project_root.joinpath("tests", "data", "test1.csv")
    print(file_path)
    df = ZipFips.read_csv(None)
    assert df is None


def test_read_zip_fips_text_file():
    """Test read_zip_fips_text_file with happy path input file."""
    project_root = utils.get_project_root()
    test_file = project_root.joinpath("tests", "data", "zipcty-fake.txt")
    zip_fips = ZipFips()
    df = zip_fips.read_zip_fips_text_file(test_file)
    assert not df.empty
    assert "AK" in df.statecd.values


def test_read_zip_fips_text_file_too_short():
    """Test read_zip_fips_text_file with header but no content input file."""
    project_root = utils.get_project_root()
    test_file = project_root.joinpath("tests", "data", "zipcty-too-short.txt")
    zip_fips = ZipFips()
    df = zip_fips.read_zip_fips_text_file(test_file)
    assert df.empty


def test_read_zip_fips_text_file_bad_state():
    """
    Test read_zip_fips_text_file with a bad state code.

    That leads to 00 as fips state code.
    """
    project_root = utils.get_project_root()
    test_file = project_root.joinpath("tests", "data", "zipcty-fake-state.txt")
    zip_fips = ZipFips()
    df = zip_fips.read_zip_fips_text_file(test_file)
    assert not df.empty
    assert "00" in str(df.fipsstct.values)


def test_read_zip_fips_text_file_bad_content():
    """Test read_zip_fips_text_file with content line that won't match RE."""
    project_root = utils.get_project_root()
    test_file = project_root.joinpath("tests", "data", "zipcty-bad-data.txt")
    zip_fips = ZipFips()
    df = zip_fips.read_zip_fips_text_file(test_file)
    assert df.empty


def test_read_zip_fips_text_file_repeat_zip_code():
    """Test read_zip_fips_text_file with repeated ZIP code."""
    project_root = utils.get_project_root()
    test_file = project_root.joinpath("tests", "data", "zipcty-test.txt")
    zip_fips = ZipFips()
    df = zip_fips.read_zip_fips_text_file(test_file)
    assert not df.empty
    assert "TX" in df.statecd.values


def test_files_to_csv():
    """Test files_to_csv with test files."""
    project_root = utils.get_project_root()
    test_file_path = project_root.joinpath("tests", "data")
    zip_fips = ZipFips()
    df = zip_fips.files_to_csv(test_file_path)
    assert not df.empty
    assert "TX" in df.statecd.values
