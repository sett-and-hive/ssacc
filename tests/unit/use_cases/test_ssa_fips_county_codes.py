""" Test SSA FIPS County Codes use cases. """

from ssacc.factories.factory import Factory, InjectionKeys
from ssacc.use_cases.ssa_fips_county_codes import build_ssa_and_fips_county_code_dataframe

GET_SSA_FIPS_CC_DF_CALLED = False


def test_build_ssa_and_fips_county_code_dataframe():
    """Test build_ssa_and_fips_county_code_dataframe."""

    def mock_get_df():
        """Mock for get_ssa_fips_cc_df()."""
        global GET_SSA_FIPS_CC_DF_CALLED
        GET_SSA_FIPS_CC_DF_CALLED = True

    Factory.register(InjectionKeys.COUNTYRATE_SSA_FIPS_CC, mock_get_df)
    build_ssa_and_fips_county_code_dataframe()

    global GET_SSA_FIPS_CC_DF_CALLED
    assert GET_SSA_FIPS_CC_DF_CALLED is True
