"""Read and clean SSA and FIPS county code records."""

from ssacc.factories.factory import Factory, InjectionKeys
from ssacc.wrappers.timing_wrapper import timing

# Busiess logic here.  No knowledge of files or databases


@timing
def build_ssa_and_fips_county_code_dataframe():
    """Build the ssa cc + fips cc dataframe."""
    get_ssa_fips_cc_df = Factory.get(InjectionKeys.COUNTYRATE_SSA_FIPS_CC)
    return get_ssa_fips_cc_df()
