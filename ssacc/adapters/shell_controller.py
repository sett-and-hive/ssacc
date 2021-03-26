"""
Shell controller for SSA County Code crosswalk.
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

import argparse

# from ssacc.clean_df import CleanDF
from ssacc.map_ssa_zip_fips import MapSsaZipFips
from ssacc.use_cases import (
    create_ssa_fips_zip,
    regenerate_zip_fips_county_codes,
    ssa_fips_county_codes,
)
from ssacc.utils import utils
from ssacc.validate_map import ValidateMap
from ssacc.wrappers.timing_wrapper import timing

# Todo: Since shell_cotroller.py is in an outer ring (external),
#  it should not know about all of these.
# Develop use cases and entities with the business logical
#  and connect to the outside (CLI, I/O) with adapters


def parse_args() -> argparse.Namespace:
    """Parse user command line arguments."""
    parser = argparse.ArgumentParser(
        prog="ssacc",
        description="Map SSA County Codes to ZIP Codes.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-r",
        type=int,
        required=False,
        default=0,
        help="Regenerate the ZIP to FIPS county code CSV, if -r 1.",
    )
    return parser.parse_args()


@timing
def shell():
    """
    Build SSA CC to FIPS CC mapping.
    Build ZIP to FIPS CC mapping.
    Build joined ZIP, FIPS CC, SSA CC.
    Add city, state.
    Build verification SSA CC to ZIP CSV.
    Build refined SSA CC (3 and 5 digit) to ZIP CSV.
    """
    args = parse_args()

    project_root = utils.get_project_root()

    # Build CSV of SSA and FIPS codes
    df_ssa_fips = ssa_fips_county_codes.build_ssa_and_fips_county_code_dataframe()
    print(df_ssa_fips.columns.values)
    print(df_ssa_fips.head())

    # ZIPs and FIPS.
    # Build a new ZIP and FIPS CSV if asked.
    # Takes about 5 minutes locally
    if args.r:
        # use case: regerate Zip Fips CSV (zipcounty.csv)
        regenerate_zip_fips_county_codes.regerate_zip_fips_county_code_data()
    # create SSA FIPS ZIPS csv
    file_path, df_map_result = create_ssa_fips_zip.create_ssa_fips_zip_csv(df_ssa_fips)
    # Validate the ZIP SSA table.
    result = ValidateMap.validate(file_path)
    if not result:
        print("Failed data validation test")  # ToDo: Print this in red in a Presenter
    else:
        print("Data quality tests pass")  # ToDo: print this in green with Colorama
        print("Writing refined ZIP to SSA County Code CSV")
        refined_file_path = project_root.joinpath("data", "ssa_cnty_zip.csv")
        MapSsaZipFips.write_refined_csv(df_map_result, refined_file_path)
    print("Running about 150 seconds locally.")
