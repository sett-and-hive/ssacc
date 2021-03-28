"""Create the merged SSA CC, FIPS CC, ZIP Codedata set."""

# # Read the ZIP and FIPS.
# ## vvv Use Case: create SSA FIPS ZIPS csv
# file_path = project_root.joinpath("data", "temp", "zipcounty.csv")
# df_zip_fips = zip_fips.read_csv(file_path)
# print(file_path)
# print(df_zip_fips.head())
# # Read the ZIP and city name.
# file_path = project_root.joinpath("data", "source", "zipcodes.csv")
# df_zip_codes = zip_fips.read_csv(file_path)
# print(file_path)
# print(df_zip_codes.head())
# # Merge DFs to create ZIP SSA table.
# df_map_1 = MapSsaZipFips.map_ssa_zip(df_ssa_fips, df_zip_fips)
# df_map_2 = MapSsaZipFips.map_city(df_map_1, df_zip_codes)
# # title case all cities, counties, states
# df_map_2 = CleanDF.titlecase_columns(df_map_2, ["city", "countyname", "state"])
# print("dfm2 head")
# print(df_map_2.head())
# # drop duplicate rows
# df_map_2 = df_map_2.drop_duplicates()
# # sort by zip then county code
# df_map_2 = df_map_2.sort_values(by=["zip", "ssacnty"])
# file_path = project_root.joinpath("data", "temp", "ssa_zip_fips.csv")
# df_map_result = MapSsaZipFips.write_csv(df_map_2, file_path)
# ### ^^^ create SSA FIPS ZIPS csv

# Maybe the entity is the final merged data set
# Maybe the operatable dataframes

import pandas as pd

from ssacc.clean_df import CleanDF
from ssacc.factories.factory import Factory, InjectionKeys
from ssacc.map_ssa_zip_fips import MapSsaZipFips
from ssacc.utils import utils
from ssacc.wrappers.timing_wrapper import timing

# Busiess logic here.  No knowledge of files or databases


@timing
def create_ssa_fips_zip_csv(df_ssa_fips):
    """Create the SSA cc+FIPS cc+ZIP Code data set."""
    df_zip_fips = create_fips_zip_dataframe()
    print(df_zip_fips.head())
    # Read the ZIP and city name.
    df_zip_codes = create_zip_city_dataframe()
    print(df_zip_codes.head())
    # Merge DFs to create ZIP SSA table.
    # df_map_1 = MapSsaZipFips.map_ssa_zip(df_ssa_fips, df_zip_fips)
    df_map_1 = merge_dataframes_on_fipscounty(df_ssa_fips, df_zip_fips)
    # df_map_2 = MapSsaZipFips.map_city(df_map_1, df_zip_codes)
    df_map_2 = merge_dataframes_on_zip_code(df_map_1, df_zip_codes)
    # title case all cities, counties, states
    df_map_2 = CleanDF.titlecase_columns(df_map_2, ["city", "countyname", "state"])
    print("dfm2 head")
    print(df_map_2.head())
    # drop duplicate rows
    df_map_2 = df_map_2.drop_duplicates()
    # sort by zip then county code
    df_map_2 = df_map_2.sort_values(by=["zip", "ssacnty"])
    project_root = utils.get_project_root()
    file_path = project_root.joinpath("data", "temp", "ssa_zip_fips.csv")
    df_map_result = MapSsaZipFips.write_csv(df_map_2, file_path)
    return file_path, df_map_result


@timing
def create_fips_zip_dataframe():
    """Build the fips cc + ZIP code dataframe.

    Dataframe should contain these columns:

    - zip The 5 digit ZIP code
    - fipscc The 3 digit FIPS county code
    - fipsstct The 5 digit FIPS state and county code
    - statecd The 2 letter state postal code
    - county The name of the county
    """
    # file_path = project_root.joinpath("data", "temp", "zipcounty.csv")
    # get df_zip_fips from gateway = zip_fips.read_csv(file_path)
    get_fips_zip_df = Factory.get(InjectionKeys.ZIPCOUNTY_READ)
    df = get_fips_zip_df()

    return df


@timing
def create_zip_city_dataframe():
    """Build the ZIP code + city name dataframe.

    Dataframe should contain these columns:

    - Zipcode The 5 digit ZIP code
    - City The name of the primary city in the ZIP code
    - State The 2 letter postal code for the city
    """
    # file_path = project_root.joinpath("data", "temp", "zipcounty.csv")
    # get df_zip_fips from ateway = zip_fips.read_csv(file_path)
    get_zip_codes_df = Factory.get(InjectionKeys.ZIPCODES_READ)
    df = get_zip_codes_df()

    return df


# # Merge DFs to create ZIP SSA table.
# df_map_1 = MapSsaZipFips.map_ssa_zip(df_ssa_fips, df_zip_fips)
# df_map_2 = MapSsaZipFips.map_city(df_map_1, df_zip_codes)


@timing
def merge_dataframes_on_fipscounty(df_ssa_fip, df_zip_fips):
    """Merge date frame to join SSA anf FIPS county codes with ZIP codes.

    - df_ssa_fip - dataframe with SSA and FIPS county codes
    - df_zip_fips - dataframe with ZIP and FIPS county codes
    """
    try:
        dfm = pd.merge(
            df_ssa_fip, df_zip_fips, how="outer", left_on="fipsstco", right_on="fipsstct"
        )
    except KeyError:
        dfm = None
    print(dfm)
    return dfm


@timing
def merge_dataframes_on_zip_code(dfs, dfz):
    """Merge data frames to add city names.

    - dfs - dataframe with ZIP, SSA and FIPS county codes
    - dfz - dataframe with ZIP and city name
    """
    try:
        dfm = pd.merge(dfs, dfz, how="outer", left_on="zip", right_on="Zipcode")
        # Pandas should be in entity not use case
        dfm = CleanDF.rename_columns(dfm, ["City"], ["city"])
        # gateways should clean column names before delivering to use case
    except KeyError:
        dfm = None
    print(dfm)
    return dfm
