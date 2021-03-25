"""Gateway to the zipcounty.csv data."""

from contextlib import suppress
import os

import pandas as pd
from pandas.io.parsers import ParserError

from ssacc.factories.factory import Factory, InjectionKeys
from ssacc.utils import utils
from ssacc.wrappers.timing_wrapper import timing


def assure_zipcounty_path():
    """Make sure path to zipcounty data exists."""
    project_root = utils.get_project_root()
    file_path = project_root.joinpath("data", "temp")
    os.makedirs(file_path, exist_ok=True)
    return file_path


def get_zipcounty_filepath():
    """Inject filepath to zipcounty data."""
    project_root = utils.get_project_root()
    file_path = project_root.joinpath("data", "temp", "zipcounty.csv")
    return file_path


# @timing
# def files_to_csv(self, input_folder_path):
#     """Read some files, build a data frame."""
#     print("ZipFips.files_to_csv")  # This is basically a gateway to a CSV file
#     project_root = Path(input_folder_path)
#     df = pd.DataFrame(columns=["zip", "fipscc", "fipsstct", "statecd", "county"])
# The usps_zipcty_gateway should return a df in the above format

#     output_file_folder = project_root.parent.joinpath("temp")
#     os.makedirs(output_file_folder, exist_ok=True)
#     output_file_path = output_file_folder.joinpath("zipcounty.csv")
#     print(f"Writing to {output_file_path}")
#     with suppress(FileNotFoundError):
#         os.remove(output_file_path)
#     df.to_csv(path_or_buf=output_file_path, index=False)
#     return df


@timing
def write_zipcounty_csv(df):
    """Create zipcounty.csv data file."""
    assure_zipcounty_path()
    get_filepath = Factory.get(InjectionKeys.ZIPCOUNTY_FILEPATH)
    output_file_path = get_filepath()
    print(f"Write zipcounty.csv data to {output_file_path}")
    with suppress(FileNotFoundError):
        os.remove(output_file_path)
    df.to_csv(path_or_buf=output_file_path, index=False)  # ToDo: use humble obect here
    return df


def read_zipcounty_csv():
    """Read zipcounty.csv and return a dataframe."""
    get_filepath = Factory.get(InjectionKeys.ZIPCOUNTY_FILEPATH)
    input_file_path = get_filepath()
    print(f"Read zipcounty.csv data from {input_file_path}")
    # Humble method to read_csv
    try:
        df = pd.read_csv(filepath_or_buffer=input_file_path, header=0, dtype=str)
        return df
    except FileNotFoundError:
        print(f"File {input_file_path} not found")
    except ParserError:
        print(f"Parser error {input_file_path} ")
    except Exception as exception:
        print(f"Any other error reading {input_file_path}")
        print(exception)
        raise
    return None
