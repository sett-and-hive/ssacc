""" Test ValidateMap."""
from contextlib import suppress
import os
from pathlib import Path
import warnings

# suppress spurious "numpy.ufunc size changed" warnings
# According to
# https://stackoverflow.com/questions/40845304/runtimewarning-numpy-dtype-size-changed-may-indicate-binary-incompatibility
# these warnings are benign.
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", message="numpy.dtype size changed")
    warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
    import pandas as pd


from ssacc.validate_map import ValidateMap

# Tests do not need to be DRY
# pylint: disable=duplicate-code
# pylint: disable=R0801


def test_construction():
    """ Test the constructor. Trivial."""
    assert ValidateMap()


def test_read_csv():
    """Test read_csv() on the happy path."""
    project_root = Path(__file__).parents[1]
    file_path = project_root.joinpath("data", "test1.csv")
    print(file_path)
    required_columns = {"ssacounty", "rating", "year", "runtime"}
    df = ValidateMap.read_csv(file_path)
    assert not df.empty
    for column_name in required_columns:
        assert column_name in df.columns


def test_read_csv_file_not_found():
    """Test read_csv() for bad path."""
    project_root = Path(__file__).parents[1]
    file_path = project_root.joinpath("data", "file_not_found.csv")
    print(file_path)
    df = ValidateMap.read_csv(file_path)
    assert df is None


def test_read_csv_exception():
    """ Test read_csv() for bad data frame. """
    project_root = Path(__file__).parents[1]
    file_path = project_root.joinpath("data", "test1.csv")
    print(file_path)
    df = ValidateMap.read_csv(None)
    assert df is None


def test_write_csv(tmpdir):
    """ Test write to CSV. """
    df = _create_dataframe_for_test_write_csv()
    project_root = Path(tmpdir)
    output_file_path = project_root.joinpath("test_validate_write_csv.csv")
    with suppress(FileNotFoundError):
        os.remove(output_file_path)
    ValidateMap.write_csv(df, output_file_path)
    assert os.path.isfile(output_file_path)


def _create_dataframe_for_test_write_csv():
    """ Create a dataframe for test_write_csv. """
    cars = {
        "zip": [220, 250, 270, 350],
        "ssacounty": [22, 25, 27, 35],
        "countyname": [2, 3, 4, 5],
        "county": [220, 250, 270, 350],
        "stabbr": [22, 25, 27, 35],
        "statecd": [2, 3, 4, 5],
        "state": [220, 250, 270, 350],
        "city": [22, 25, 27, 35],
        "fipscc": [2, 3, 4, 5],
        "fipsstco": [22, 25, 27, 35],
        "fipsstct": [2, 3, 4, 5],
    }
    df = pd.DataFrame(
        cars,
        columns=[
            "zip",
            "ssacounty",
            "countyname",
            "county",
            "stabbr",
            "statecd",
            "state",
            "city",
            "fipscc",
            "fipsstco",
            "fipsstct",
        ],
    )
    return df


def test_validate_all_zips():
    """ Test validate_all_zips. """
    to_check = _create_dataframe_with_zipcodes_to_test()
    known_zips = _create_dataframe_with_known_zipcodes()
    missing_zips = ValidateMap.validate_all_zips(to_check, known_zips)
    assert missing_zips.empty


def test_validate_all_zips_some_zips_missing():
    """ Test validate_all_zips. """
    to_check = _create_dataframe_with_empty_zipcodes_to_test()
    known_zips = _create_dataframe_with_known_zipcodes()
    missing_zips = ValidateMap.validate_all_zips(to_check, known_zips)
    assert not missing_zips.empty


def _create_dataframe_with_known_zipcodes():
    """ Create dataframe of some known ZIP codes for test_validate_all_zips. """
    df = pd.DataFrame(
        {
            "Zipcode": ["00705", "00611", "00610", "00612"],
            "ZipType": ["Standard", "PO Box", "Private", "Military"],
        },
        columns=["Zipcode", "ZipType"],
    )
    return df


def _create_dataframe_with_zipcodes_to_test():
    """ Create dataframe of sample ZIP codes for test_validate_all_zips. """
    df = pd.DataFrame({"zip": ["00705", "00610", "00611", "00612"]}, columns=["zip"])
    return df


def _create_dataframe_with_empty_zipcodes_to_test():
    """Create dataframe of sample ZIP codes with missing values
    for test_validate_all_zips_some_zips_missing."""
    df = pd.DataFrame({"zip": ["00705"]}, columns=["zip"])
    return df
