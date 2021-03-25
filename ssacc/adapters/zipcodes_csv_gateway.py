"""Gateway to the zipcodes.csv data."""

import pandas as pd
from pandas.io.parsers import ParserError

from ssacc.factories.factory import Factory, InjectionKeys
from ssacc.utils import utils


def get_zipcodes_filepath():
    """Inject filepath to zipcounty data."""
    project_root = utils.get_project_root()
    file_path = project_root.joinpath("data", "source", "zipcodes.csv")
    return file_path


def read_zipcodes_csv():
    """Read zipcodes.csv and return a dataframe."""
    get_filepath = Factory.get(InjectionKeys.ZIPCODES_FILEPATH)
    input_file_path = get_filepath()
    print(f"Read zipcodes.csv data from {input_file_path}")
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
