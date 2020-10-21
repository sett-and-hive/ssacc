"""

get zip and fips from one file
get fips and ssa from another file
get zips and cities from another file
map them together

assumes you ran fetch script to populate the data folders

TODO: refactor this into a pipeline runner for a
filter and pipes architecture that is more testable.

"""
import argparse
from pathlib import Path
import sys

from clean_df import CleanDF
from map_ssa_zip_fips import MapSsaZipFips
from ssa_fips import SsaFips
from validate_map import ValidateMap
from zip_fips import ZipFips

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())


def parse_args() -> argparse.Namespace:
    """Parse user command line arguments."""
    parser = argparse.ArgumentParser(
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


def main():
    """
    Build SSA CC to FIPS CC mapping.
    Build ZIP to FIPS CC mapping.
    Build joined ZIP, FIPS CC, SSA CC.
    Add city, state.
    Build verification SSA CC to ZIP CSV.
    Build refined SSA CC (3 and 5 digit) to ZIP CSV.
    """

    project_root = Path(__file__).resolve().parents[1]
    args = parse_args()
    """
    Build CSV of SSA and FIPS codes
    """
    file_path = project_root.joinpath("data", "source", "countyrate.csv")
    dfs = SsaFips.read_ssa_fips(file_path)
    print(dfs.columns.values)
    print(file_path)
    print(dfs.head())
    """
    ZIPs and FIPS
    """

    """
    Build a new ZIP and FIPS CSV if asked
    """
    if args.r:
        project_root = Path(__file__).parents[1]  # was 2
        file_path = project_root.joinpath("data", "source")
        print(f"root file path {file_path}")
        ZipFips.files_to_csv(file_path)
    """ Read the ZIP and FIPS """
    file_path = project_root.joinpath("data", "temp", "zipcounty.csv")
    dfz = ZipFips.read_csv(file_path)
    print(file_path)
    print(dfz.head())
    """ Read the ZIP and city name """
    file_path = project_root.joinpath("data", "source", "zipcodes.csv")
    dfc = ZipFips.read_csv(file_path)
    print(file_path)
    print(dfc.head())
    """ Merge DFs to create ZIP SSA table"""
    dfm1 = MapSsaZipFips.map_ssa_zip(dfs, dfz)
    dfm2 = MapSsaZipFips.map_city(dfm1, dfc)
    # title case all cities, counties, states
    dfm2 = CleanDF.titlecase_columns(dfm2, ["city", "countyname", "state"])
    print("dfm2 head")
    print(dfm2.head())
    # drop duplicate rows
    dfm2 = dfm2.drop_duplicates()
    # sort by zip then county code
    dfm2 = dfm2.sort_values(by=["zip", "ssacnty"])
    file_path = project_root.joinpath("data", "temp", "ssa_zip_fips.csv")
    dfr = MapSsaZipFips.write_csv(dfm2, file_path)
    """ Validate the ZIP SSA table"""
    b = ValidateMap.validate(file_path)
    if not b:
        print("Failed data validation test")
    else:
        print("Data quality tests pass")
        print("Writing refined ZIP to SSA County Code CSV")
        refined_file_path = project_root.joinpath("data", "ssa_cnty_zip.csv")
        MapSsaZipFips.write_refined_csv(dfr, refined_file_path)
    return None


# Allow the script to be run standalone (useful during development in PyCharm).
if __name__ == "__main__":
    sys.exit(main())
