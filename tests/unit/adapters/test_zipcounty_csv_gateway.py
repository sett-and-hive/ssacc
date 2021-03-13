"""Test gateway to zipcounty.csv data."""

import os
import warnings

# suppress spurious "numpy.ufunc size changed" warnings
# According to
# https://stackoverflow.com/questions/40845304/runtimewarning-numpy-dtype-size-changed-may-indicate-binary-incompatibility
# these warnings are benign.
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", message="numpy.dtype size changed")
    warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
    import pandas as pd

from ssacc.adapters import zipcounty_csv_gateway
from ssacc.factories.factory import Factory, InjectionKeys

# Tests do not need to be DRY
# pylint: disable=duplicate-code
# pylint: disable=R0801
# globals OK in these mocks
# pylint: disable=W0603

GET_PATH_CALLED = False
ZIPCOUNTY_READ_CALLED = False
ZIPCOUNTY_WRITE_CALLED = False


def setup_function():
    """Pytest setup function."""
    global GET_PATH_CALLED
    global ZIPCOUNTY_READ_CALLED
    global ZIPCOUNTY_WRITE_CALLED
    GET_PATH_CALLED = False
    ZIPCOUNTY_READ_CALLED = False
    ZIPCOUNTY_WRITE_CALLED = False
    Factory.reset()


def teardown_function():
    """Pytest teardown function."""
    Factory.reset()


def test_assume_zipcounty_epath():
    """Make sure it returns a path that is valid and does exist."""
    path = zipcounty_csv_gateway.assure_zipcounty_path()
    assert path
    assert os.path.isdir(path)


def test_get_zipcounty_filepath():
    """Make sure it returns a filepath that is valid but may not exist."""
    file_path = zipcounty_csv_gateway.get_zipcounty_filepath()
    assert file_path


def test_write_zipcounty_csv():
    """Test write_zipcounty_csv on the happy path."""

    def mock_get_zipcounty_filepath():
        """Mock for get_zipcounty_filepath()."""
        global GET_PATH_CALLED
        GET_PATH_CALLED = True
        return "test_csv_path"

    states = {"name": ["Wisconsin"], "code": ["WI"]}
    df = pd.DataFrame(states, columns=["name", "code"])

    Factory.register(InjectionKeys.ZIPCOUNTY_FILEPATH, mock_get_zipcounty_filepath)
    zipcounty_csv_gateway.write_zipcounty_csv(df)

    assert GET_PATH_CALLED is True


def test_read_zipcounty_csv():
    """Test read_zipcounty_csv on the happy path."""

    def mock_get_zipcounty_filepath():
        """Mock for get_zipcounty_filepath()."""
        global GET_PATH_CALLED
        GET_PATH_CALLED = True
        return "test_csv_path"

    Factory.register(InjectionKeys.ZIPCOUNTY_FILEPATH, mock_get_zipcounty_filepath)
    zipcounty_csv_gateway.read_zipcounty_csv()

    assert GET_PATH_CALLED is True
