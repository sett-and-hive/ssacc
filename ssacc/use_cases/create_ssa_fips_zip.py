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

from ssacc.factories.factory import Factory, InjectionKeys
from ssacc.wrappers.timing_wrapper import timing

# Busiess logic here.  No knowledge of files or databases


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
    # get df_zip_fips from ateway = zip_fips.read_csv(file_path)
    get_fips_zip_df = Factory.get(InjectionKeys.ZIPCOUNTY_READ)
    df = get_fips_zip_df()

    return df


@timing
def create_zip_city_dataframe():
    """Build the ZIP code + city name dataframe.

    Dataframe should contain these columns:

    - Zipcode The 5 digit ZIP code
    - City The ame of the primary city in the ZIP code
    - State The 2 letter postal code for the city
    """
    # file_path = project_root.joinpath("data", "temp", "zipcounty.csv")
    # get df_zip_fips from ateway = zip_fips.read_csv(file_path)
    get_zip_codes_df = Factory.get(InjectionKeys.ZIPCODES_READ)
    df = get_zip_codes_df()

    return df
