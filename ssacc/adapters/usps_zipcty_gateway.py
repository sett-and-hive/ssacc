"""
    Gateway to read USPS ZIP-FIPS county code-mapping flat files.

    These files are from https://wonder.cdc.gov/wonder/sci_data/datasets/zipcty[A|B].zip
        # use case: regerate Zip Fips CSV (zipcounty.csv)
        # project_root = Path(__file__).parents[2]  # should be project path?
        file_path = project_root.joinpath("data", "source")
        print(f"root file path {file_path}")
        # two gateways  - 1 to read files, 1 to write new csv
        zip_fips.files_to_csv(file_path)
"""

import os
import re

import pandas as pd

from ssacc.factories.factory import Factory, InjectionKeys
from ssacc.utils import utils
from ssacc.wrappers.timing_wrapper import timing


def get_zipcty_path():
    """Inject path to USPS zipcty data."""
    project_root = utils.get_project_root()
    path = project_root.joinpath("data", "source")
    return path


# TODO clean up path of reading zipcty and assembling that DF
# From writin that to a CSV
# From reading that new CSV
# This adapter only read the zipcty data and the old zipfips CSV is other data for another


@timing
def get_zip_fips_cc_df():
    """Return clean ZIP and FIPS county codes in a dataframe."""
    # We expect a DF with these columns=["zip", "fipscc", "fipsstct", "statecd", "county"]
    get_path = Factory.get(InjectionKeys.USPS_ZIPCTY_PATH)
    input_path = get_path()
    print(f"reading zipcty files from {input_path}")
    read_files = Factory.get(InjectionKeys.USPS_ZIPCTY_READ)
    df = read_files(input_path)
    print(df.head())
    # df1 = clean_ssa_fips_data(df)
    # print(df1.head())
    # df2 = rename_ssacounty_column(df1)
    # df3 = split_ssacnty_column(df2)
    return df


@timing
def read_zipcty_files(input_path):
    """Read zipcty files."""
    # ToDo: make it read
    # We expect a DF with these columns=["zip", "fipscc", "fipsstct", "statecd", "county"]
    df = pd.DataFrame(columns=["zip", "fipscc", "fipsstct", "statecd", "county"])
    # The usps_zipcty_gateway should return a df in the above format
    print(input_path)
    frames = [
        read_zip_fips_text_file(input_path.joinpath(filename))
        for filename in os.listdir(input_path)
        if filename.startswith("zipcty")
    ]
    df = df.append(frames)
    if not df.empty:
        print("Head of zip county df")
        print(df.head())
    else:
        print("Oh no. zip county df is empty")
    return df


# TODO: refactor to reduce complexity and local variable count
@timing
def read_zip_fips_text_file(input_file_path):
    """Read text file with ZIPS and FIPS codes."""
    # Gateway to a specialized text data file
    with open(input_file_path) as zip_county_file:
        zip_county_lines = zip_county_file.readlines()
    # Business logic to extract ZipFips data frame
    # if we treat the file as an external database, then the
    # gateway can know how to return the desired data frame
    # The interface is to return a data frame with
    # columns=["zip", "fipscc", "fipsstct", "statecd", "county"]
    # TODO: statecodes come from another ateway - how to get them over here?
    # or is that telling me something? lke only this gateway needs the statecodes?
    # are the statecodes implict in the zipcty data and we can use that?
    # statecodes data in this cotext map state two letter code to state fips
    # which does not belong in a gateway to zipcty.
    get_statecodes = Factory.get(InjectionKeys.GET_STATE_JSON)
    statecodes = get_statecodes()
    df = parse_zip_counties(zip_county_lines, statecodes)
    return df


@timing
def parse_zip_counties(lines, statecodes):
    """Parse columns from ZIP FIPS data."""
    # Compromise plan
    # 1) call statecode gateway directly from here to make it work
    # 2) refactor one of two ways
    # 2A) stop using regex and use fixed widths to extract fields
    # 2B) let the use case handle the statecodes to add statefips to county fips
    zip_seen = {}
    df = pd.DataFrame(columns=["zip", "fipscc", "fipsstct", "statecd", "county"])
    # Field Description https://wonder.cdc.gov/wonder/sci_data/codes/fips/type_txt/cntyxref.asp
    #   FIELD
    #   SEQUENCE                                          RELATIVE
    #                 FIELD                    LOGICAL    POSITION
    #   NUMBER        DESCRIPTION              LENGTH     FROM THRU    CONTENT NOTES
    #      1          ZIP CODE                   05         01    as
    #      2          UPDATE KEY NO              10         06    15
    #      3              ZIP ADD ON LOW NO
    #                        ZIP SECTOR NO       02         16    17
    #                        ZIP SEGMENT NO      02         18    19
    #      4             ZIP ADD ON HIGH NO
    #                        ZIP SECTOR NO       02         20    21
    #                        ZIP SEGMENT NO      02         22    23
    #      5          STATE ABBREV               02         24    25
    #      6          COUNTY NO                  03         26    28
    #      7          COUNTY NAME                25         29    53
    for zip_county_line in lines[1:]:  # skip first line
        match_result = re.match(
            r"(?P<zip>.{5}).{18}(?P<state>..)(?P<fips>...)(?P<county>[\w. ]+)",
            zip_county_line,
        )
        if match_result:
            groupdict_result = match_result.groupdict()
            test = str(groupdict_result["zip"]).zfill(5) + str(groupdict_result["fips"]).zfill(3)
            if test not in zip_seen:
                df_len = len(df)
                zip_code = str(groupdict_result["zip"]).zfill(5)
                fips = str(groupdict_result["fips"]).zfill(3)
                try:
                    fips_st_ct = str(statecodes[groupdict_result["state"]]).zfill(2)
                except KeyError:
                    print(
                        f"KeyError adding state code to {fips} "
                        f"in {groupdict_result['state']}. Zeroing"
                    )
                    fips_st_ct = "00"
                    # There is at least one record with missing state code. Carry on
                fips_st_ct += fips
                state = str(groupdict_result["state"])
                county = str(groupdict_result["county"]).rstrip()
                to_append = [zip_code, fips, fips_st_ct, state, county]
                zip_seen[test] = to_append
                df.loc[df_len] = to_append
    return df
