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

from ssacc.clean_df import CleanDF
from ssacc.map_ssa_zip_fips import MapSsaZipFips
from ssacc.use_cases import regenerate_zip_fips_county_codes, ssa_fips_county_codes
from ssacc.utils import utils
from ssacc.validate_map import ValidateMap
from ssacc.wrappers.timing_wrapper import timing
from ssacc.zip_fips import ZipFips

# Todo: Since cli.py is in an outer ring (external),
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

    """
    Build CSV of SSA and FIPS codes
    """
    # file_path = project_root.joinpath("data", "source", "countyrate.csv")
    # df_ssa_fips = SsaFips.read_ssa_fips(file_path)
    # first try at use_cases
    df_ssa_fips = ssa_fips_county_codes.build_ssa_and_fips_county_code_dataframe()
    print(df_ssa_fips.columns.values)
    print(df_ssa_fips.head())

    # ZIPs and FIPS.
    # Build a new ZIP and FIPS CSV if asked.
    # Takes about 5 minutes locally
    zip_fips = ZipFips()
    if args.r:
        # use case: regerate Zip Fips CSV (zipcounty.csv)
        regenerate_zip_fips_county_codes.regerate_zip_fips_county_code_data()
    # Read the ZIP and FIPS.
    file_path = project_root.joinpath("data", "temp", "zipcounty.csv")
    df_zip_fips = zip_fips.read_csv(file_path)
    print(file_path)
    print(df_zip_fips.head())
    # Read the ZIP and city name.
    file_path = project_root.joinpath("data", "source", "zipcodes.csv")
    df_zip_codes = zip_fips.read_csv(file_path)
    print(file_path)
    print(df_zip_codes.head())
    # Merge DFs to create ZIP SSA table.
    df_map_1 = MapSsaZipFips.map_ssa_zip(df_ssa_fips, df_zip_fips)
    df_map_2 = MapSsaZipFips.map_city(df_map_1, df_zip_codes)
    # title case all cities, counties, states
    df_map_2 = CleanDF.titlecase_columns(df_map_2, ["city", "countyname", "state"])
    print("dfm2 head")
    print(df_map_2.head())
    # drop duplicate rows
    df_map_2 = df_map_2.drop_duplicates()
    # sort by zip then county code
    df_map_2 = df_map_2.sort_values(by=["zip", "ssacnty"])
    file_path = project_root.joinpath("data", "temp", "ssa_zip_fips.csv")
    df_map_result = MapSsaZipFips.write_csv(df_map_2, file_path)

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
