"""Gateway to the zipcodes.csv data."""

from ssacc.adapters import csv_utils
from ssacc.factories.factory import Factory, InjectionKeys
from ssacc.utils import utils


def get_zipcodes_filepath():
    """Inject filepath to zipcounty data."""
    project_root = utils.get_project_root()
    return project_root.joinpath("data", "source", "zipcodes.csv")


def read_zipcodes_csv():
    """Read zipcodes.csv and return a dataframe."""
    get_filepath = Factory.get(InjectionKeys.ZIPCODES_FILEPATH)
    input_file_path = get_filepath()
    print(f"Read zipcodes.csv data from {input_file_path}")
    return csv_utils.create_dataframe_from_csv(input_file_path)
