"""Test gateway to USPS ZIp Code to FIPS county code data."""

import warnings

# suppress spurious "numpy.ufunc size changed" warnings
# According to
# https://stackoverflow.com/questions/40845304/runtimewarning-numpy-dtype-size-changed-may-indicate-binary-incompatibility
# these warnings are benign.
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", message="numpy.dtype size changed")
    warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
    import pandas as pd

from ssacc.adapters import usps_zipcty_gateway
from ssacc.factories.factory import Factory, InjectionKeys

#  from ssacc.utils import utils

# Tests do not need to be DRY
# pylint: disable=duplicate-code
# pylint: disable=R0801


GET_PATH_CALLED = False
STATE_READ_CALLED = False


def setup_function():
    """Pytest setup function."""
    global GET_PATH_CALLED
    global STATE_READ_CALLED
    GET_PATH_CALLED = False
    STATE_READ_CALLED = False
    Factory.reset()


def teardown_function():
    """Pytest teardown function."""
    Factory.reset()


def test_get_zipcty_path():
    """Make sure it returns a path that is valid but may not exist."""
    file_path = usps_zipcty_gateway.get_zipcty_path()
    assert file_path


def test_get_zip_fips_cc_df():
    """Test state_fips_json on the happy path."""

    def mock_get_zipcty_path():
        """Mock for get_state_json_filepath()."""
        global GET_PATH_CALLED
        GET_PATH_CALLED = True
        return "test_json_path"

    def mock_read_zip_fips_filepath(mock_input_path):
        """Mock for get_state_json_filepath()."""
        global STATE_READ_CALLED
        STATE_READ_CALLED = True
        states = {"name": ["Wisconsin"], "code": ["WI"]}
        df = pd.DataFrame(states, columns=["name", "code"])
        return df

    Factory.register(InjectionKeys.USPS_ZIPCTY_PATH, mock_get_zipcty_path)
    Factory.register(InjectionKeys.USPS_ZIPCTY_READ, mock_read_zip_fips_filepath)

    usps_zipcty_gateway.get_zip_fips_cc_df()

    assert GET_PATH_CALLED is True
    assert STATE_READ_CALLED is True
