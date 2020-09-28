from contextlib import suppress
import os
from pathlib import Path

import pandas as pd

from ssacc.clean_df import CleanDF

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())


class MapSsaZipFips:
    @staticmethod
    def map_ssa_zip(dfs, dfz):
        """
        dfs - dataframe with SSA and FIPS county codes
        dfz - dataframe with ZIP and FIPS county codes
        """
        dfm = pd.merge(dfs, dfz, how="outer", left_on="fipsstco", right_on="fipsstct")
        print(dfm)
        return dfm

    @staticmethod
    def map_city(dfs, dfz):
        """
        dfs - dataframe with ZIP, SSA and FIPS county codes
        dfz - dataframe with ZIP and city name
        """
        dfm = pd.merge(dfs, dfz, how="outer", left_on="zip", right_on="Zipcode")
        dfm = CleanDF.rename_columns(dfm, ["City"], ["city"])
        print(dfm)
        return dfm

    @staticmethod
    def write_csv(df, output_file_path):
        with suppress(FileNotFoundError):
            os.remove(output_file_path)
        df = MapSsaZipFips.reorder_and_sort_data(df)
        df.to_csv(path_or_buf=output_file_path, index=0)
        return df

    @staticmethod
    def reorder_and_sort_data(df):
        # ssacounty	stabbr	countyname	fipsstco	state	year	zip	fipscc	fipsstct	statecd	county
        # change order to group
        df = CleanDF.reorder_columns(df,
                                     [
                                         "zip",
                                         "ssacnty",
                                         "ssastco",
                                         "fipscc",
                                         "fipsstco",
                                         "fipsstct",
                                         "countyname",
                                         "county",
                                         "city",
                                         "stabbr",
                                         "statecd",
                                         "state",
                                     ]
                                     )
        df = df.sort_values(by=["zip"])
        # Sanitize - drop rows with no ZIP. The point is to map ZIP to SSA CNTY CD.
        df = df.dropna(subset=["zip"])
        return df

    @staticmethod
    def write_refined_csv(df, output_file_path):
        with suppress(FileNotFoundError):
            os.remove(output_file_path)
        # clean out columns we don't need
        df = MapSsaZipFips.clean_refined_data(df)
        df.to_csv(path_or_buf=output_file_path, index=0)

    @staticmethod
    def clean_refined_data(df):
        df = CleanDF.drop_columns(df, ["fipscc", "fipsstco", "fipsstct", "county", "statecd"])
        # Sanitize - drop rows with no ZIP. The point is to map ZIP to SSA CNTY CD.
        # Sanitize - drop rows with no ssacnty. The point is to map ZIP to SSA CNTY CD.
        # Sanitize - drop rows were city is None.
        # Why not to worry about ZIP Code 00401 anymore:
        # https://www.quora.com/What-is-the-lowest-ZIP-code-and-what-is-the-highest-ZIP-code-in-America
        df = CleanDF.dropna_rows(df, ["zip", "ssacnty", "city"])
        print(df.head())
        return df
