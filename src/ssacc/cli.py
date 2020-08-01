"""

get zip and fips from one file
get fips and ssa from another file
map them together

assumes you ran fetch script to populate the data folders

"""
import argparse
from pathlib import Path
import sys

from ssacc.map_ssa_zip_fips import MapSsaZipFips
from ssacc.ssa_fips import SsaFips
from ssacc.validate_map import ValidateMap
from ssacc.zip_fips import ZipFips


def parse_args() -> argparse.Namespace:
    """Parse user command line arguments."""
    parser = argparse.ArgumentParser(
        description="Map SSA County Codes to ZIP codes.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-r",
        type=int,
        required=False,
        default=0,
        help="Regenerate the ZIP to FIPS county code CSV.",
    )
    return parser.parse_args()


def main():
    """
    Build ZIP to FIPS CC CSV
    Build SSA CC to FIPS CC mapping.
    Build ZIP to FIPS CC mapping.
    Build verification SSA CC to ZIP CSV.
    Build refined SSA CC (3 and 5 digit) to ZIP CSV.
    """

    project_root = Path(__file__).parents[2]
    args = parse_args()
    """
    Build CSV of SSA and FIPS codes
    """
    file_path = project_root.joinpath("data", "source", "countyrate.csv")
    s = SsaFips()
    dfs = s.csv_read(file_path)
    print(dfs.columns.values)
    print(file_path)
    print(dfs.head())
    """
    ZIPs and FIPS
    """
    z = ZipFips()
    """
    Build a new ZIP and FIPS CSV if asked
    """
    if args.r:
        project_root = Path(__file__).parents[2]
        file_path = project_root.joinpath("data", "source")
        z.read_files(file_path)
    """ Read the ZIP and FIPS """
    file_path = project_root.joinpath("data", "temp", "zipcounty.csv")
    dfz = z.read_csv(file_path)
    print(file_path)
    print(dfz.head())
    """ Merge DF to create ZIP SSA table"""
    m = MapSsaZipFips()
    dfm = m.map_it(dfs, dfz)
    file_path = project_root.joinpath("data", "temp", "ssa_zip_fips.csv")
    dfr = m.write_csv(dfm, file_path)
    """ Validate the ZIP SSA table"""
    v = ValidateMap()
    b = v.validate(file_path)
    if not b:
        print("Failed data validation test")
    else:
        print("Data quality tests pass")
        print("Writing refined ZIP to SSA County Code CSV")
        refined_file_path = project_root.joinpath("data", "ssa_cnty_zip.csv")
        m.write_refined_csv(dfr, refined_file_path)
    return


# Allow the script to be run standalone (useful during development in PyCharm).
if __name__ == "__main__":
    sys.exit(main())
