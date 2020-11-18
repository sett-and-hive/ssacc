"""Validate the combined CSV file. Some data engineering."""
from contextlib import suppress
import os
from pathlib import Path

import numpy as np
import pandas as pd
from pandas.io.parsers import ParserError

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())


class ValidateMap:

    """Validate the data mappings in the filters building up the final output."""

    @staticmethod
    def validate(input_file_name):
        """Validate the penultimate file."""
        dfm = ValidateMap.read_csv(input_file_name)
        project_root = Path(input_file_name).parents[1]
        test_file_name = project_root.joinpath("source", "zipcodes.csv")
        dft = ValidateMap.read_csv(test_file_name)
        print(dft.head())
        #
        print("validate all zips")
        df_missing = ValidateMap.validate_all_zips(dfm, dft)
        b_1 = df_missing.empty
        if not b_1:
            print("Failed ZIP test")
            missing_file_name = project_root.joinpath("temp", "missing_zipcodes.csv")
            print(f"Storing missing ZIP codes in {missing_file_name}")
            df_missing.to_csv(path_or_buf=missing_file_name, index=0)
        #
        print("validate all fips")
        b_2 = ValidateMap.validate_all_fips_state_county_codes(dfm)
        if not b_2:
            print("Failed FIPS test")
        #
        print("validate all county names")
        b_3 = ValidateMap.validate_all_county_names(dfm)
        if not b_3:
            print("Failed county name test")
        #
        print("validate all state codes")
        b_4 = ValidateMap.validate_all_state_codes(dfm)
        if not b_4:
            print("Failed state code test")
        #
        print("validate all ZIPs have SSA County Codes")
        b_5 = ValidateMap.validate_all_zips_have_ssacnty(dfm)
        if not b_5:
            print("Failed ssa for ZIP test")
        return b_2 and b_4 and b_5
        # TODO: Fix ZIP and return b_1
        # TODO: Fix stuff and return b_3

    @staticmethod
    def write_csv(df, output_file_path):
        """Write the csf from the data frame."""
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
                "city",
            ]
        ]
        df.to_csv(path_or_buf=output_file_path, index=0)

    @staticmethod
    def read_csv(input_file_path):
        """Create a dataframe from a csv file."""
        try:
            df = pd.read_csv(filepath_or_buffer=input_file_path, header=0, dtype=str)
            return df
        except FileNotFoundError:
            print(f"File {input_file_path} not found")
        except ParserError:
            print(f"Parser error {input_file_path} ")
            # continue
        except Exception:
            print(f"Any other error reading {input_file_path}")
        return None

    @staticmethod
    def validate_all_zips(dfm, dft):
        """Validate ZIP codes in SSA FIP ZIP csv.

        dfm - dataframe with SSA CC, FIP CC and ZIP
              generated by this program.
        dft - dataframe of all known ZIP codes

        returns df_ missing
                a dataframe in the format of dft with
                rows for the ZIP codes not found in dfm.
        """
        dft = dft.sort_values(by=["Zipcode"])
        df_missing = pd.DataFrame().reindex(columns=dft.columns)
        found = 0
        missing = 0
        total = 0
        count = len(dft)
        for i in range(count):
            try:
                df_zip_code = dft.iloc[[i]]
                zip_code = df_zip_code["Zipcode"].to_string(index=False).strip()
                try:
                    zip_found = dfm[dfm["zip"] == zip_code]
                    if not zip_found.empty:
                        found += 1
                    else:
                        df_missing = df_missing.append(df_zip_code, ignore_index=True)
                        missing += 1
                    total += 1
                except KeyError:
                    print(f"Could not find ZIP code {zip_code} in SSA map")
                    missing += 1
                    total += 1
                    continue
            except KeyError:
                print(f"Error looking for ZIP code in test file at position{i}")
        print(
            "ZIP codes in sample: ",
            f"Found {found}. ",
            f"Missing {missing}. ",
            f"Total {total}. Expect 42522.",
        )
        return df_missing

    # There are 3141 countries in the US
    # cite: https://thehill.com/opinion/white-house/
    #       525488-if-joe-biden-wants-to-unite-america-he-must-do-this-immediately
    # Make sure we have them all

    @staticmethod
    def validate_all_county_names(dfm):
        """Validate the county names."""
        missing = 0
        total = 0
        count = len(dfm)
        for i in range(count):
            # TODO: make sure this use of df.loc is correct
            countyname = dfm.loc[i, "countyname"]
            countytest = "".join(filter(str.isalnum, str(countyname)))
            countytest = str(countytest).upper()
            # TODO: make sure this use of df.loc is correct
            county = dfm.loc[i, "county"]
            county = "".join(filter(str.isalnum, str(county)))
            # print(f"Is {countytest} in {county}")
            try:
                if (countytest in county) or (county in countytest):
                    total += 1
                else:
                    missing += 1
                    total += 1
            except IndexError:
                print("bad county data [{countytest}] [{county}]")
                missing += 1
                total += 1
        print(
            f"Missing county names count {missing}. Expect 739. Total count {total}. Expect 53881."
        )
        return True if 0 == missing else False

    @staticmethod
    def validate_all_fips_state_county_codes(dfm):
        """Validate FIPS county codes."""
        missing = 0
        total = 0
        count = len(dfm)
        for i in range(count):
            # TODO: make sure this use of df.loc is correct
            fips = dfm.loc[i, "fipsstco"]
            try:
                dfm.loc[dfm["fipsstct"] == fips]
                total += 1
            except KeyError:
                print(f"Count not find SSA fips {fips} in SSA map")
                missing += 1
                total += 1
            except FileNotFoundError:
                pass
        print(f"Missing fips count {missing}. Total count {total}. Expect 53881.")
        return missing == 0

    @staticmethod
    def validate_all_state_codes(dfm):
        """Validate state codes.

        There are two sources of state code and we want
        to test to see that they match when all the
        required data is present.
        """
        state_compare = np.where(dfm["stabbr"] == dfm["statecd"], True, False)
        dfm["st_compare"] = state_compare
        dfm["FullCnty"] = True
        # TODO: make sure this use of df.loc is correct
        dfm.loc[dfm["ssacnty"].isnull(), "FullCnty"] = False
        dfm["Test"] = dfm["st_compare"] == dfm["FullCnty"]
        print(dfm)
        missing_state_country = np.where(~dfm["Test"], True, False)
        missing_list = missing_state_country.tolist()
        missing = missing_list.count(True)
        total = len(missing_list)
        print(f"Missing state code+cnty count {missing}. Total count {total}. Expect 53881.")
        return missing == 0

    @staticmethod
    def validate_all_zips_have_ssacnty(dfm):
        """Make sure ZIP codes have a SSA county code."""
        print(dfm.head())
        missing = 0
        total = 0
        count = len(dfm)
        for i in range(count):
            try:
                # TODO: make sure this use of df.loc is correct
                zip_code = dfm.loc[i, "zip"]
                try:
                    # TODO: make sure this use of df.loc is correct
                    dfm.loc[i, "ssacnty"]
                    total += 1
                except KeyError:
                    print(f"Count not find SSA County code for {zip_code} in SSA map")
                    missing += 1
                    total += 1
                    continue
                except ValueError:
                    print(f"Count not find SSA County code value for {zip_code} in SSA map")
                    missing += 1
                    total += 1
                    continue
            except KeyError:
                print(f"Error looking for ZIP in main file at position{i}")
        print(f"Missing SSA count {missing}. Total count {total}. Expect 53881.")
        return missing == 0
