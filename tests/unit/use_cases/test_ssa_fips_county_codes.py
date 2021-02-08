""" Test SSA FIPS County Codes use cases. """

from ssacc.factories.factory import Factory, InjectionKeys
from ssacc.use_cases.ssa_fips_county_codes import build_ssa_and_fips_county_code_dataframe

get_ssa_fips_cc_df_called = False


def test_build_ssa_and_fips_county_code_dataframe():
    def mock_get_df():
        global get_ssa_fips_cc_df_called
        get_ssa_fips_cc_df_called = True

    Factory.register(InjectionKeys.COUNTYRATE_SSA_FIPS_CC, mock_get_df)
    build_ssa_and_fips_county_code_dataframe()

    global get_ssa_fips_cc_df_called
    assert get_ssa_fips_cc_df_called is True
