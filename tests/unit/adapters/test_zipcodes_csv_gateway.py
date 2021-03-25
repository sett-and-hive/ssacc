"""Test gateway to zipcodes.csv data."""

from ssacc.adapters import zipcodes_csv_gateway
from ssacc.factories.factory import Factory, InjectionKeys

# Tests do not need to be DRY
# pylint: disable=duplicate-code
# pylint: disable=R0801
# globals OK in these mocks
# pylint: disable=W0603

GET_PATH_CALLED = False
ZIPCODE_READ_CALLED = False


def setup_function():
    """Pytest setup function."""
    global GET_PATH_CALLED
    global ZIPCODE_READ_CALLED
    GET_PATH_CALLED = False
    ZIPCODE_READ_CALLED = False
    Factory.reset()


def teardown_function():
    """Pytest teardown function."""
    Factory.reset()


def test_get_zipcode_filepath():
    """Make sure it returns a filepath that is valid but may not exist."""
    file_path = zipcodes_csv_gateway.get_zipcodes_filepath()
    assert file_path


def test_read_zipcodes_csv():
    """Test read_zipcodes_csv on the happy path."""

    def mock_get_zipcounty_filepath():
        """Mock for get_zipcode_filepath()."""
        global GET_PATH_CALLED
        GET_PATH_CALLED = True
        return "test_csv_path"

    Factory.register(InjectionKeys.ZIPCODES_FILEPATH, mock_get_zipcounty_filepath)
    zipcodes_csv_gateway.read_zipcodes_csv()

    assert GET_PATH_CALLED is True
