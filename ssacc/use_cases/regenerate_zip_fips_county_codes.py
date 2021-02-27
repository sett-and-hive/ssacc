"""Regenerate CSV with ZIP codes and FIPS county codes."""

from ssacc.factories.factory import Factory, InjectionKeys

#         / gateway to input files
# Use case
#         \ gateway to write csv


def regerate_zip_fips_county_code_data():
    """Regenerate ZIP to FIPS county code crosswalk."""
    get_zip_fips_cc_df = Factory.get(InjectionKeys.GET_USPS_ZIP_FIPS_CC)
    df = get_zip_fips_cc_df()
    put_zip_fips_cc_df = Factory.get(InjectionKeys.WRITE_ZIP_FIPS_CC)
    put_zip_fips_cc_df(df)
