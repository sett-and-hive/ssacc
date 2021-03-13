"""Gateway to the countyrate.csv data."""

import pandas as pd

from ssacc.clean_df import CleanDF
from ssacc.factories.factory import Factory, InjectionKeys
from ssacc.utils import utils
from ssacc.wrappers.timing_wrapper import timing


def get_countyrate_filepath():
    """Inject filepath to countyrate data."""
    project_root = utils.get_project_root()
    file_path = project_root.joinpath("data", "source", "countyrate.csv")
    return file_path


@timing
def get_ssa_fips_cc_df():
    """Return clean SSA and FIPS county codes in a dataframe."""
    get_filepath = Factory.get(InjectionKeys.COUNTYRATE_FILEPATH)
    input_file_path = get_filepath()
    print(f"opening {input_file_path}")
    df = read_csv(input_file_path)
    print(df.head())
    df1 = clean_ssa_fips_data(df)
    print(df1.head())
    df2 = rename_ssacounty_column(df1)
    df3 = split_ssacnty_column(df2)
    return df3


def read_csv(input_file_path):
    """Read data from CSV file."""
    try:
        df = pd.read_csv(filepath_or_buffer=input_file_path, header=0, dtype=str)
        return df
    except FileNotFoundError as exception:
        print(f"File {input_file_path} not found.")
        raise exception


@timing
def clean_ssa_fips_data(df):
    """Clean up SSA FIPS county code data."""
    df = CleanDF.drop_columns(
        df,
        [
            "partsab5bonus2018rate",
            "partsab35bonus2018rate",
            "partsab0bonus2018rate",
            "partsabesrd2018rate",
        ],
    )
    return df


def split_ssacnty_column(df):
    """Add column ssacnty with 3 digit SSA county code: strip off state code from ssastco."""
    df["ssacnty"] = df["ssastco"].str[2:]
    print(df.head())
    return df


def rename_ssacounty_column(df):
    """Change misleading name of 'ssacounty' column."""
    df = CleanDF.rename_columns(df, ["ssacounty"], ["ssastco"])  # SSA STate COunty
    print(df.head())
    return df
