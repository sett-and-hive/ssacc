import pandas as pd
from pandas.io.parsers import ParserError


class StringConverter:
    class StringConverter(dict):
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return str

        def get(self, default=None):
            return str


class SsaFips:
    @staticmethod
    def csv_read(input_file_path):
        # Read data from file 'filename.csv'
        # (in the same directory that your python process is based)
        # Control delimiters, rows, column names with read_csv (see later)
        try:
            df = pd.read_csv(filepath_or_buffer=input_file_path, header=0, dtype=str,)
            # clean out
            df.drop("partsab5bonus2018rate", axis=1, inplace=True)
            df.drop("partsab35bonus2018rate", axis=1, inplace=True)
            df.drop("partsab0bonus2018rate", axis=1, inplace=True)
            df.drop("partsabesrd2018rate", axis=1, inplace=True)
            # change misleading name
            df.rename(columns={"ssacounty": "ssastco"}, inplace=True)
            # add column with 3 digit SSA county code (strip off state code)
            df["ssacnty"] = df["ssastco"].str[2:]
            # Preview the first 5 lines of the loaded data
            print(df.head())
            return df
        except FileNotFoundError:
            print(f"File {input_file_path} not found")
        except ParserError:
            print(f"Parser error {input_file_path} ")
        except Exception:
            print(f"Any other error reading {input_file_path}")
        return
