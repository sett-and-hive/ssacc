"""Test gateway to state FIPS JSON data."""

import warnings

# suppress spurious "numpy.ufunc size changed" warnings
# According to
# https://stackoverflow.com/questions/40845304/runtimewarning-numpy-dtype-size-changed-may-indicate-binary-incompatibility
# these warnings are benign.
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", message="numpy.dtype size changed")
    warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
    import pandas as pd

from ssacc.adapters import state_json_gateway
from ssacc.factories.factory import Factory, InjectionKeys

#  from ssacc.utils import utils

# Tests do not need to be DRY
# pylint: disable=duplicate-code
# pylint: disable=R0801

GET_PATH_CALLED = False
JSON_READ_CALLED = False


def setup_function():
    global GET_PATH_CALLED
    global JSON_READ_CALLED
    GET_PATH_CALLED = False
    JSON_READ_CALLED = False
    Factory.reset()


def teardown_function():
    Factory.reset()


def test_get_state_json_filepath():
    """Make sure it returns a filepath that is valid but may not exist."""
    file_path = state_json_gateway.get_state_json_filepath()
    assert file_path


def test_get_state_fips_json():
    """Test state_fips_json on the happy path."""

    def mock_get_state_json_filepath():
        """Mock for get_state_json_filepath()."""
        global GET_PATH_CALLED
        GET_PATH_CALLED = True
        return "test_json_path"

    def mock_read_state_json_filepath(mock_input_path):
        """Mock for get_state_json_filepath()."""
        global JSON_READ_CALLED
        JSON_READ_CALLED = True
        zip_fips = {"zipcode": [2015, 2013, 2018, 2019], "fipsstct": [22000, 25000, 27000, 35000]}
        df = pd.DataFrame(zip_fips, columns=["zipcode", "fipsstct"])
        return df

    Factory.register(InjectionKeys.STATE_JSON_FILEPATH, mock_get_state_json_filepath)
    Factory.register(InjectionKeys.STATE_JSON_READ, mock_read_state_json_filepath)
    state_json_gateway.get_state_fips_json()

    assert GET_PATH_CALLED is True
    assert JSON_READ_CALLED is True
