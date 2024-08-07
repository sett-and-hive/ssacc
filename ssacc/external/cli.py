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

from ssacc.adapters import (
    countyrate_gateway,
    shell_controller,
    state_json_gateway,
    usps_zipcty_gateway,
    zipcodes_csv_gateway,
    zipcounty_csv_gateway,
)
from ssacc.factories.factory import Factory, InjectionKeys
from ssacc.use_cases import create_ssa_fips_zip


def setup_factory():
    """Set up dependency injection."""
    # County rate data gateway
    Factory.register(InjectionKeys.COUNTYRATE_SSA_FIPS_CC, countyrate_gateway.get_ssa_fips_cc_df)
    Factory.register(InjectionKeys.COUNTYRATE_FILEPATH, countyrate_gateway.get_countyrate_filepath)
    # State code JSON data gateway
    Factory.register(InjectionKeys.STATE_JSON_FILEPATH, state_json_gateway.get_state_json_filepath)
    Factory.register(InjectionKeys.STATE_JSON_READ, state_json_gateway.read_state_json)
    Factory.register(InjectionKeys.GET_STATE_JSON, state_json_gateway.get_state_fips_json)
    # USPS ZIP FIPS data gateway
    Factory.register(InjectionKeys.USPS_ZIPCTY_PATH, usps_zipcty_gateway.get_zipcty_path)
    Factory.register(InjectionKeys.USPS_ZIPCTY_READ, usps_zipcty_gateway.read_zipcty_files)
    Factory.register(InjectionKeys.GET_USPS_ZIP_FIPS_CC, usps_zipcty_gateway.get_zip_fips_cc_df)
    # zipcounty CSV data gateway
    Factory.register(
        InjectionKeys.ZIPCOUNTY_FILEPATH, zipcounty_csv_gateway.get_zipcounty_filepath
    )
    Factory.register(InjectionKeys.ZIPCOUNTY_READ, zipcounty_csv_gateway.read_zipcounty_csv)
    Factory.register(InjectionKeys.ZIPCOUNTY_WRITE, zipcounty_csv_gateway.write_zipcounty_csv)
    # zipcodes CSV data gateway
    Factory.register(InjectionKeys.ZIPCODES_FILEPATH, zipcodes_csv_gateway.get_zipcodes_filepath)
    Factory.register(InjectionKeys.ZIPCODES_READ, zipcodes_csv_gateway.read_zipcodes_csv)
    # SSA FIPS ZIP CSV data gateway
    Factory.register(
        InjectionKeys.SSAFIPZIPS_FILEPATH, create_ssa_fips_zip.get_ssa_zip_fips_file_path
    )


# Allow the script to be run standalone.
if __name__ == "__main__":
    setup_factory()
    shell_controller.shell()
