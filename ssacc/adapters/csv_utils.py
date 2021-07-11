"""Utility functions to read CSV files."""

import pandas as pd
from pandas.errors import ParserError


def create_dataframe_from_csv(input_file_path: str):
    """Read CSV into dataframe."""
    # Consider Humble method to read_csv
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
