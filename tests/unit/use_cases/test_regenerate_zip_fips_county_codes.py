"""Test SSA FIPS County Codes use cases. """

from ssacc.factories.factory import Factory, InjectionKeys
from ssacc.use_cases.regenerate_zip_fips_county_codes import regerate_zip_fips_county_code_data

GET_ZIP_FIPS_CC_DF_CALLED = False
PUT_ZIP_FIPS_CC_DF_CALLED = False


def test_regerate_zip_fips_county_code_data():
    """Test regerate_zip_fips_county_code_data."""

    def mock_get_df():
        """Mock for get_ssa_fips_cc_df()."""
        global GET_ZIP_FIPS_CC_DF_CALLED
        GET_ZIP_FIPS_CC_DF_CALLED = True

    def mock_put_df(df):
        """Mock for put_ssa_fips_cc_df()."""
        global PUT_ZIP_FIPS_CC_DF_CALLED
        PUT_ZIP_FIPS_CC_DF_CALLED = True

    Factory.register(InjectionKeys.GET_USPS_ZIP_FIPS_CC, mock_get_df)
    Factory.register(InjectionKeys.WRITE_ZIP_FIPS_CC, mock_put_df)
    regerate_zip_fips_county_code_data()

    assert GET_ZIP_FIPS_CC_DF_CALLED is True
    assert PUT_ZIP_FIPS_CC_DF_CALLED is True
