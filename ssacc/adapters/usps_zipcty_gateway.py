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

#  from ssacc.clean_df import CleanDF
from ssacc.factories.factory import Factory, InjectionKeys
from ssacc.utils import utils
from ssacc.wrappers.timing_wrapper import timing


def get_zipcty_path():
    """Inject path to USPS zipcty data."""
    project_root = utils.get_project_root()
    path = project_root.joinpath("data", "source")
    return path


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
    pass  # ToDo: make it read
    # We expect a DF with these columns=["zip", "fipscc", "fipsstct", "statecd", "county"]
    #     df = pd.DataFrame(columns=["zip", "fipscc", "fipsstct", "statecd", "county"])
    # The usps_zipcty_gateway should return a df in the above format
    #     print(project_root)
    #     frames = [
    #         self.read_zip_fips_text_file(project_root.joinpath(filename))
    #         for filename in os.listdir(project_root)
    #         if filename.startswith("zipcty")
    #     ]
    #     df = df.append(frames)
    #     if df is not None:
    #         print("Head of zip county df")
    #         print(df.head())
    #     else:
    #         print("Oh no. zip county df is None")
