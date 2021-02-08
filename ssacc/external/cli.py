"""
SSA County Code crosswalk application context

The application will:
get zip and fips from one file.
get fips and ssa from another file.
get zips and cities from another file.
map them together.

assumes you ran fetch script to populate the data folders.

TODO: refactor this into a pipeline runner for a
filter and pipes architecture that is more testable.
https://github.com/MicrosoftDocs/architecture-center/blob/master/docs/patterns/pipes-and-filters.md

"""

import sys

from ssacc.adapters import countyrate_gateway, shell_controller
from ssacc.factories.factory import Factory, InjectionKeys


def setup_factory():
    """Set up dependency injection."""
    Factory.register(InjectionKeys.COUNTYRATE_SSA_FIPS_CC, countyrate_gateway.get_ssa_fips_cc_df)
    Factory.register(InjectionKeys.COUNTYRATE_FILEPATH, countyrate_gateway.get_countyrate_filepath)


# Allow the script to be run standalone.
if __name__ == "__main__":
    setup_factory()
    shell_controller.shell(sys.argv)
