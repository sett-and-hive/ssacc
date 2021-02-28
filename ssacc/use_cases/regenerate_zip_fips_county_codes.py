"""Regenerate CSV with ZIP codes and FIPS county codes."""

from ssacc.factories.factory import Factory, InjectionKeys
from ssacc.wrappers.timing_wrapper import timing

#         / gateway to input files
# Use case
#         \ gateway to write csv


@timing
def regerate_zip_fips_county_code_data():
    """Regenerate ZIP to FIPS county code crosswalk."""
    get_zip_fips_cc_df = Factory.get(InjectionKeys.GET_USPS_ZIP_FIPS_CC)
    # We expect a DF with these columns=["zip", "fipscc", "fipsstct", "statecd", "county"]
    df = get_zip_fips_cc_df()
    put_zip_fips_cc_df = Factory.get(InjectionKeys.WRITE_ZIP_FIPS_CC)
    put_zip_fips_cc_df(df)
