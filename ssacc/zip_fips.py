"""
Map ZIP Codes and FIPS county codes.

Inspired by https://github.com/bgruber/zip2fips/blob/master/makejson.py
"""
from contextlib import suppress
import json
import os
from pathlib import Path
import re

import pandas as pd
from pandas.io.parsers import ParserError

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())


class ZipFips:
    """Build intermediate ZIP and FIPS county code data frame."""

    def __init__(self):
        project_root = Path(__file__).parents[1]
        state_file = project_root.joinpath("reference", "state_fips.json")
        self.statecodes = json.load(open(state_file))

    def files_to_csv(self, input_folder_path):
        """Read some files, build a data frame."""
        print("ZipFips.files_to_csv")
        project_root = Path(input_folder_path)
        df = pd.DataFrame(columns=["zip", "fipscc", "fipsstct", "statecd", "county"])

        print(project_root)
        frames = [
            self.read_zip_fips_text_file(project_root.joinpath(filename))
            for filename in os.listdir(project_root)
            if filename.startswith("zipcty")
        ]
        df = df.append(frames)
        if df is not None:
            print("Head of zip county df")
            print(df.head())
        else:
            print("Oh no. zip county df is None")
        output_file_folder = project_root.parent.joinpath("temp")
        os.makedirs(output_file_folder, exist_ok=True)
        output_file_path = output_file_folder.joinpath("zipcounty.csv")
        print(f"Writing to {output_file_path}")
        with suppress(FileNotFoundError):
            os.remove(output_file_path)
        df.to_csv(path_or_buf=output_file_path, index=False)
        return df

    @staticmethod
    def read_csv(input_file_path):
        """Read data from a CSV into a data frame."""
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

    def read_zip_fips_text_file(self, input_file_path):
        zip_seen = {}
        df = pd.DataFrame(columns=["zip", "fipscc", "fipsstct", "statecd", "county"])
        zip_county_file = open(input_file_path)
        zip_county_file.readline()  # skip first line
        for zip_county_line in zip_county_file:
            match_result = re.match(
                r"(?P<zip>.{5}).{18}(?P<state>..)(?P<fips>...)(?P<county>[\w. ]+)", zip_county_line
            )
            if match_result:
                groupdict_result = match_result.groupdict()
                test = str(groupdict_result["zip"]).zfill(5) + str(groupdict_result["fips"]).zfill(
                    3
                )
                if test not in zip_seen:
                    df_len = len(df)
                    zip_code = str(groupdict_result["zip"]).zfill(5)
                    fips = str(groupdict_result["fips"]).zfill(3)
                    try:
                        fips_st_ct = str(self.statecodes[groupdict_result["state"]]).zfill(2)
                    except KeyError:
                        print(
                            f"KeyError adding state code to {fips} "
                            f"in {groupdict_result['state']}. Zeroing"
                        )
                        fips_st_ct = "00"
                        # There is at least one record with missing state code. Carry on
                    fips_st_ct += fips
                    state = str(groupdict_result["state"])
                    county = str(groupdict_result["county"]).rstrip()
                    to_append = [zip_code, fips, fips_st_ct, state, county]
                    zip_seen[test] = to_append
                    df.loc[df_len] = to_append
        return df
