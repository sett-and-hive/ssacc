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

from ssacc.adapters import (
    countyrate_gateway,
    shell_controller,
    state_json_gateway,
    usps_zipcty_gateway,
)
from ssacc.factories.factory import Factory, InjectionKeys


def setup_factory():
    """Set up dependency injection."""
    Factory.register(InjectionKeys.COUNTYRATE_SSA_FIPS_CC, countyrate_gateway.get_ssa_fips_cc_df)
    Factory.register(InjectionKeys.COUNTYRATE_FILEPATH, countyrate_gateway.get_countyrate_filepath)
    Factory.register(
        InjectionKeys.GET_USPS_ZIP_FIPS_CC, countyrate_gateway.get_countyrate_filepath
    )
    Factory.register(InjectionKeys.WRITE_ZIP_FIPS_CC, countyrate_gateway.get_countyrate_filepath)
    Factory.register(InjectionKeys.STATE_JSON_FILEPATH, state_json_gateway.get_state_json_filepath)
    Factory.register(InjectionKeys.STATE_JSON_READ, state_json_gateway.read_state_json)
    Factory.register(InjectionKeys.USPS_ZIPCTY_PATH, usps_zipcty_gateway.get_zipcty_path)
    Factory.register(InjectionKeys.USPS_ZIPCTY_READ, usps_zipcty_gateway.read_zipcty_files)


# Allow the script to be run standalone.
if __name__ == "__main__":
    setup_factory()
    shell_controller.shell(sys.argv)
