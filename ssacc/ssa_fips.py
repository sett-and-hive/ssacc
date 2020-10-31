"""Read and clean SSA and FIPS county codes."""
from pathlib import Path

import pandas as pd
from pandas.io.parsers import ParserError

from ssacc.clean_df import CleanDF

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())


class SsaFips:
    @staticmethod
    def read_ssa_fips(input_file_path):
        """Read data then clean it up."""
        df = SsaFips.read_csv(input_file_path)
        df1 = SsaFips.clean_ssa_fips_data(df)
        print(df1.head())
        return df1

    @staticmethod
    def read_csv(input_file_path):
        """Read data from CSV file."""
        try:
            df = pd.read_csv(filepath_or_buffer=input_file_path, header=0, dtype=str)
            return df
        except FileNotFoundError:
            print(f"File {input_file_path} not found")
        except ParserError:
            print(f"Parser error {input_file_path} ")
        except Exception:
            print(f"Any other error reading {input_file_path}")
        return None

    # TODO Refactor with clean_df methods
    @staticmethod
    def clean_ssa_fips_data(df):
        """ Clean up SSA FIPS county code data."""
        df = CleanDF.drop_columns(
            df,
            [
                "partsab5bonus2018rate",
                "partsab35bonus2018rate",
                "partsab0bonus2018rate",
                "partsabesrd2018rate",
            ],
        )
        # change misleading name
        df = CleanDF.rename_columns(df, ["ssacounty"], ["ssastco"])  # SSA STate COunty
        # add column ssacnty with 3 digit SSA county code: strip off state code from ssastco
        df["ssacnty"] = df["ssastco"].str[2:]
        # Preview the first 5 lines of the loaded data
        print(df.head())
        return df
