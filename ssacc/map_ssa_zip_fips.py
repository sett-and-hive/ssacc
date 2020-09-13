from contextlib import suppress
import os
from pathlib import Path

import pandas as pd

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())


class MapSsaZipFips:
    @staticmethod
    def map_it(dfs, dfz):
        # dfs - dataframe with SSA and FIPS county codes
        # dfz - dataframe with ZIP and FIPS county codes
        dfm = pd.merge(dfs, dfz, how="outer", left_on="fipsstco", right_on="fipsstct")
        print(dfm)
        return dfm

    @staticmethod
    def map_city(dfs, dfz):
        # dfs - dataframe with ZIP, SSA and FIPS county codes
        # dfz - dataframe with ZIP and city name
        dfm = pd.merge(dfs, dfz, how="outer", left_on="zip", right_on="Zipcode")
        print(dfm)
        return dfm

    @staticmethod
    def write_csv(df, output_file_path):
        with suppress(FileNotFoundError):
            os.remove(output_file_path)
        # ssacounty	stabbr	countyname	fipsstco	state	year	zip	fipscc	fipsstct	statecd	county
        # change order to group
        df = df[
            [
                "zip",
                "ssacnty",
                "ssastco",
                "fipscc",
                "fipsstco",
                "fipsstct",
                "countyname",
                "county",
                "stabbr",
                "city",
                "statecd",
                "state",
            ]
        ]
        df = df.sort_values(by=["zip"])
        # Sanitize - drop rows with no ZIP. The point is to map ZIP to SSA CNTY CD.
        df = df.dropna(subset=["zip"])
        df.to_csv(path_or_buf=output_file_path, index=0)
        return df

    @staticmethod
    def write_refined_csv(df, output_file_path):
        with suppress(FileNotFoundError):
            os.remove(output_file_path)
        # clean out
        df.drop("fipscc", axis=1, inplace=True)
        df.drop("fipsstco", axis=1, inplace=True)
        df.drop("fipsstct", axis=1, inplace=True)
        df.drop("county", axis=1, inplace=True)
        df.drop("statecd", axis=1, inplace=True)
        # Sanitize - drop rows with no ZIP. The point is to map ZIP to SSA CNTY CD.
        df = df.dropna(subset=["zip"])
        # Sanitize - drop rows with no ssacnty. The point is to map ZIP to SSA CNTY CD.
        df = df.dropna(subset=["ssacnty"])
        # Sanatize - drop rows were city is None
        # Why not to worry about 00401 anymore
        # https://www.quora.com/What-is-the-lowest-ZIP-code-and-what-is-the-highest-ZIP-code-in-America
        df = df.dropna(subset=["city"])
        print(df.head())
        df.to_csv(path_or_buf=output_file_path, index=0)
