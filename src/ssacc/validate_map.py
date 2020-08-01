"""Validate the combined CSV file. Some data engineering"""

from contextlib import suppress
import os
from pathlib import Path
import pandas as pd
from pandas.io.parsers import ParserError


class ValidateMap:
    def validate(self, input_file_name):
        dfm = self.read_csv(input_file_name)
        project_root = Path(input_file_name).parents[1]
        test_file_name = project_root.joinpath("source", "zipcodes.csv")
        dft = self.read_csv(test_file_name)
        print(dft.head())
        #
        print("validate all zips")
        b1 = self.validate_all_zips(dfm, dft)
        if not b1:
            print("Failed ZIP test")
        #
        print("validate all fips")
        b2 = self.validate_all_fips_state_county_codes(dfm)
        if not b2:
            print("Failed FIPS test")
        #
        print("validate all county names")
        b3 = self.validate_all_county_names(dfm)
        if not b3:
            print("Failed county name test")
        #
        print("validate all state codes")
        b4 = self.validate_all_state_codes(dfm)
        if not b4:
            print("Failed state code test")
        #
        print("validate all ZIPs have SSA County Codes")
        b5 = self.validate_all_zips_have_ssacnty(dfm)
        if not b5:
            print("Failed ssa for ZIP test")
        return b1 and b2 and b4 and b5

    @staticmethod
    def write_csv(df, output_file_path):
        with suppress(FileNotFoundError):
            os.remove(output_file_path)
        # ssacounty	stabbr	countyname	fipsstco	state	year	zip	fipscc	fipsstct	statecd	county
        # change order to group
        df = df[
            [
                "zip",
                "ssacounty",
                "fipscc",
                "fipsstco",
                "fipsstct",
                "countyname",
                "county",
                "stabbr",
                "statecd",
                "state",
            ]
        ]
        df.to_csv(path_or_buf=output_file_path, index=0)

    @staticmethod
    def read_csv(input_file_path):
        try:
            df = pd.read_csv(filepath_or_buffer=input_file_path, header=0, dtype=str,)
            return df
        except FileNotFoundError:
            print(f"File {input_file_path} not found")
        except ParserError:
            print(f"Parser error {input_file_path} ")
            # continue
        except Exception:
            print(f"Any other error reading {input_file_path}")
            # continue
        return

    @staticmethod
    def validate_all_zips(dfm, dft):
        dft = dft.sort_values(by=["Zipcode"])
        print(dfm.head())
        missing = 0
        total = 0
        count = len(dft)
        for i in range(count):
            try:
                zip = dft.loc[i, "Zipcode"]
                try:
                    rows = dfm.loc[dfm["zip"] == zip]
                    # print(row)
                    total += 1
                except KeyError:
                    print(f"Count not find zip {zip} in SSA map")
                    missing += 1
                    total += 1
                    continue
                except FileNotFoundError:
                    pass
            except KeyError:
                print(f"Error looking for zip in test file at position{i}")
        print(f"Missing zip count {missing}. Total count {total}")
        return True if 0 == missing else False

    @staticmethod
    def validate_all_county_names(dfm):
        missing = 0
        total = 0
        count = len(dfm)
        for i in range(count):
            countyname = dfm.loc[i, "countyname"]
            countytest = "".join(filter(str.isalnum, str(countyname)))
            countytest = str(countytest).upper()
            county = dfm.loc[i, "county"]
            county = "".join(filter(str.isalnum, str(county)))
            # print(f"Is {countytest} in {county}")
            try:
                if (countytest in county) or (county in countytest):
                    total += 1
                else:
                    missing += 1
                    total += 1
            except:
                print("bad county data [{countytest}] [{county}]")
                missing += 1
                total += 1
        print(f"Missing county names count {missing}. Total count {total}")
        return True if 0 == missing else False

    @staticmethod
    def validate_all_fips_state_county_codes(dfm):
        missing = 0
        total = 0
        count = len(dfm)
        for i in range(count):
            fips = dfm.loc[i, "fipsstco"]
            try:
                rows = dfm.loc[dfm["fipsstct"] == fips]
                # print(row)
                total += 1
            except KeyError:
                print(f"Count not find SSA fips {fips} in SSA map")
                missing += 1
                total += 1
            except FileNotFoundError:
                pass
        print(f"Missing fips count {missing}. Total count {total}")
        return True if 0 == missing else False

    @staticmethod
    def validate_all_state_codes(dfm):
        missing = 0
        total = 0
        count = len(dfm)
        for i in range(count):
            state = dfm.loc[i, "stabbr"]
            try:
                rows = dfm.loc[dfm["statecd"] == state]
                # print(row)
                total += 1
            except KeyError:
                print(f"Count not find statecd {stabbr} in SSA map")
                missing += 1
                total += 1
            except FileNotFoundError:
                pass
        print(f"Missing state code count {missing}. Total count {total}")
        return True if 0 == missing else False

    @staticmethod
    def validate_all_zips_have_ssacnty(dfm):
        print(dfm.head())
        missing = 0
        total = 0
        count = len(dfm)
        for i in range(count):
            try:
                zip = dfm.loc[i, "zip"]
                try:
                    rows = dfm.loc[i, "ssacnty"]
                    total += 1
                except KeyError:
                    print(f"Count not find SSA County code for {zip} in SSA map")
                    missing += 1
                    total += 1
                    continue
                except ValueError:
                    print(f"Count not find SSA County code value for {zip} in SSA map")
                    missing += 1
                    total += 1
                    continue
            except KeyError:
                print(f"Error looking for zip in main file at position{i}")
        print(f"Missing SSA count {missing}. Total count {total}")
        return True if 0 == missing else False
