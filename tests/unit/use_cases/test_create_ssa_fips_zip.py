"""Test create_ssa_fips_zip use case."""

from ssacc.factories.factory import Factory, InjectionKeys
from ssacc.use_cases import create_ssa_fips_zip

# Tests do not need to be DRY
# pylint: disable=duplicate-code
# pylint: disable=R0801

# globals OK in these mocks
# pylint: disable=W0603

GET_FIPS_ZIP_DF_CALLED = False
GET_ZIP_CITY_DF_CALLED = False


def test_create_fips_zip_dataframe():
    """Test create_fips_zip_dataframe."""

    def mock_get_df():
        """Mock for gateway call to get DF from data."""
        global GET_FIPS_ZIP_DF_CALLED
        GET_FIPS_ZIP_DF_CALLED = True

    Factory.register(InjectionKeys.ZIPCOUNTY_READ, mock_get_df)
    create_ssa_fips_zip.create_fips_zip_dataframe()

    assert GET_FIPS_ZIP_DF_CALLED is True


def test_create_zip_city_dataframe():
    """Test create_zip_city_dataframe."""

    def mock_get_df():
        """Mock for gateway call to get DF from data."""
        global GET_ZIP_CITY_DF_CALLED
        GET_ZIP_CITY_DF_CALLED = True

    Factory.register(InjectionKeys.ZIPCODES_READ, mock_get_df)
    create_ssa_fips_zip.create_zip_city_dataframe()

    assert GET_ZIP_CITY_DF_CALLED is True
