"""Test gateway to USPS ZIp Code to FIPS county code data."""

import os
from pathlib import Path
from unittest.mock import patch
import warnings

import numpy as np

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

# Tests do not need to be DRY
# pylint: disable=duplicate-code
# pylint: disable=R0801
# pylint: disable=W0603
# globals OK in these mocks
# pylint: disable=W0603

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

    def mock_read_zip_fips_filepath(_mock_input_path):
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


@patch("ssacc.adapters.usps_zipcty_gateway.read_zip_fips_text_file")
def test_read_zipcty_files(mock_read_zip_fips_text_file, tmp_path):
    """Test that read_zipcty_files calls read_zip_fips_text_file."""
    states = {"name": ["Wisconsin"], "code": ["WI"]}
    df = pd.DataFrame(states, columns=["name", "code"])
    mock_read_zip_fips_text_file.return_value = df

    temp_filepath = tmp_path.joinpath("zipcty.fake")
    temp_filepath.write_text("test")  # Add file for read_zipcty_files to find.
    result = usps_zipcty_gateway.read_zipcty_files(tmp_path)
    os.remove(temp_filepath)

    assert result["zip"][0] is np.nan
    assert result["name"][0] == df["name"][0]
    assert mock_read_zip_fips_text_file.called


@patch("ssacc.adapters.usps_zipcty_gateway.read_zip_fips_text_file")
def test_read_zipcty_files_empty_frame(mock_read_zip_fips_text_file, tmp_path):
    """Test that read_zipcty_files calls read_zip_fips_text_file."""
    states = {}
    df = pd.DataFrame(states, columns=["name", "code"])
    mock_read_zip_fips_text_file.return_value = df

    temp_filepath = tmp_path.joinpath("zipcty.fake")
    temp_filepath.write_text("test")  # Add file for read_zipcty_files to find.
    result = usps_zipcty_gateway.read_zipcty_files(tmp_path)
    os.remove(temp_filepath)

    assert result.empty


@patch("ssacc.adapters.usps_zipcty_gateway.parse_zip_counties")
def test_read_zip_fips_text_file(mock_parse_zip_counties, tmp_path):
    """Test that parse_zip_counties is called."""

    def mock_read_state_json():
        """Mock for get_state_json()."""
        return {}

    Factory.register(InjectionKeys.GET_STATE_JSON, mock_read_state_json)
    states = {"name": ["Iowa"], "code": ["IA"]}
    df = pd.DataFrame(states, columns=["name", "code"])
    mock_parse_zip_counties.return_value = df

    temp_filepath = tmp_path.joinpath("fake.file")
    temp_filepath.write_text("test")
    result = usps_zipcty_gateway.read_zip_fips_text_file(Path(temp_filepath))
    os.remove(temp_filepath)

    assert result["name"][0] == df["name"][0]
    assert mock_parse_zip_counties.called


def test_parse_zip_counties():
    """Test zip_parse_counties."""
    line = "00401000000000100010001NY119WESTCHESTER"
    lines = ["header", line]
    state_codes = {"NY": "36"}
    result = usps_zipcty_gateway.parse_zip_counties(lines, state_codes)

    assert result["zip"][0] == "00401"
    assert result["county"][0] == "WESTCHESTER"


def test_parse_zip_counties_bad_state_code():
    """Test zip_parse_counties with a state code not in dict."""
    line = "00401000000000100010001NY119WESTCHESTER"
    lines = ["header", line]
    state_codes = {"TX": "36"}
    result = usps_zipcty_gateway.parse_zip_counties(lines, state_codes)

    assert result["fipsstct"][0] == "00119"
