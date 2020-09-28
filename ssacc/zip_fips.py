# inspired by https://github.com/bgruber/zip2fips/blob/master/makejson.py
from contextlib import suppress
import json
import os
from pathlib import Path
import re

import pandas as pd
from pandas.io.parsers import ParserError

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())


class ZipFips:
    @staticmethod
    def read_files(input_folder_path):
        project_root = Path(input_folder_path)
        state_file = project_root.joinpath("state_fips.json")
        statecodes = json.load(open(state_file))
        zip_seen = {}
        df = pd.DataFrame(columns=["zip", "fipscc", "fipsstct", "statecd", "county"])

        print(project_root)
        for i in range(1, 11):
            file_path = project_root.joinpath(f"zipcty{i}")
            print(file_path)
            zfile = open(file_path)
            zfile.readline()  # skip first line
            for z in zfile:
                m = re.match(r"(?P<zip>.{5}).{18}(?P<state>..)(?P<fips>...)(?P<county>[\w. ]+)", z)
                if m:
                    r = m.groupdict()
                    test = str(r["zip"]).zfill(5) + str(r["fips"]).zfill(3)
                    if test not in zip_seen:
                        df_len = len(df)
                        zip_code = str(r["zip"]).zfill(5)
                        fips = str(r["fips"]).zfill(3)
                        try:
                            fips_st_ct = str(statecodes[r["state"]]).zfill(2)
                        except KeyError:
                            print(f"KeyError adding state code to {fips} in {r['state']}. Zeroing")
                            fips_st_ct = "00"
                            # There is at least one record with missing state code. Carry on
                        fips_st_ct += fips
                        state = str(r["state"])
                        county = str(r["county"]).rstrip()
                        to_append = [zip_code, fips, fips_st_ct, state, county]
                        zip_seen[test] = to_append
                        df.loc[df_len] = to_append
        output_file_path = project_root.parent.joinpath("temp", "zipcounty.csv")
        with suppress(FileNotFoundError):
            os.remove(output_file_path)
        df.to_csv(path_or_buf=output_file_path, index=0)
        return df

    @staticmethod
    def read_csv(input_file_path):
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
