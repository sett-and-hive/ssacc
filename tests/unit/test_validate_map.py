""" Test ValidateMap."""
from contextlib import suppress
import os
from pathlib import Path

import pandas as pd

from ssacc.validate_map import ValidateMap

# pylint: disable=duplicate-code
# pylint: disable=R0801
# Tests do not need to be DRY


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


def test_write_csv():
    """ Test write to CSV. """
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
    project_root = Path(__file__).parents[1]
    output_file_path = project_root.joinpath("temp", "v-test1.csv")
    with suppress(FileNotFoundError):
        os.remove(output_file_path)
    ValidateMap.write_csv(df, output_file_path)
    assert os.path.isfile(output_file_path)
