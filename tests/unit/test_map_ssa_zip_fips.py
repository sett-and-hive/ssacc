"""Test MapSsaZipFips."""
from contextlib import suppress
import os
from pathlib import Path
import warnings

import pandas as pd

# suppress spurious "numpy.ufunc size changed" warnings
# According to
# https://stackoverflow.com/questions/40845304/runtimewarning-numpy-dtype-size-changed-may-indicate-binary-incompatibility
# these warnings are benign.
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", message="numpy.dtype size changed")
    warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

from ssacc.map_ssa_zip_fips import MapSsaZipFips

# Tests do not need to be DRY
# pylint: disable=duplicate-code
# pylint: disable=R0801


CAR1 = "Honda Civic"
CAR2 = "Toyota Corolla"
CAR3 = "Ford Focus"
CAR4 = "Audi A4"


def test_construction():
    """ Test the constructor. Trivial."""
    assert MapSsaZipFips()


def test_map_ssa_zip():
    """Test Map SSA to ZIP code via FIPS county code.

    pd.merge(dfs, dfz, how="outer", left_on="fipsstco", right_on="fipsstct")
    """
    ssa_fips = {
        "ssacc": [CAR1, CAR2, CAR3, CAR4],
        "fipsstco": [22000, 25000, 27000, 35000],
        "Year": [2015, 2013, 2018, 2019],
    }
    zip_fips = {"zipcode": [2015, 2013, 2018, 2019], "fipsstct": [22000, 25000, 27000, 35000]}
    dfs = pd.DataFrame(ssa_fips, columns=["ssacc", "fipsstco", "Year"])
    dfz = pd.DataFrame(zip_fips, columns=["zipcode", "fipsstct"])
    df = MapSsaZipFips.map_ssa_zip(dfs, dfz)
    assert not df.empty
    assert str(df.fipsstco.values) in str(df.fipsstct.values)


def test_map_ssa_zip_bad():
    """
    Test Map SSA to ZIP code via FIPS county code with bad data
    pd.merge(dfs, dfz, how="outer", left_on="fipsstco", right_on="fipsstct")
    """
    ssa_fips = {
        "ssacc": [CAR1, CAR2, CAR3, CAR4],
        "xxfipsstco": [22000, 25000, 27000, 35000],
        "Year": [2015, 2013, 2018, 2019],
    }
    zip_fips = {"zipcode": [2015, 2013, 2018, 2019], "fipsstct": [22000, 25000, 27000, 35000]}
    dfs = pd.DataFrame(ssa_fips, columns=["ssacc", "xxfipsstco", "Year"])
    dfz = pd.DataFrame(zip_fips, columns=["zipcode", "fipsstct"])
    df = MapSsaZipFips.map_ssa_zip(dfs, dfz)
    assert df is None


def test_map_city():
    """
    Test mapping of city data via ZIP codes.
    This is tesing a dataframe merge where df_ssa "zip" merges
    with df_zip "Zipcode"
    df_merged = pd.merge(df_ssa, df_zip, how="outer", left_on="zip", right_on="Zipcode")
    """
    ssa_fips = {
        "City": [CAR1, CAR2, CAR3, CAR4],
        "fipsstco": [22000, 25000, 27000, 35000],
        "zip": [2015, 2013, 2018, 2019],
    }
    zip_fips = {"Zipcode": [2015, 2013, 2018, 2019], "fipsstct": [22000, 25000, 27000, 35000]}
    dfs = pd.DataFrame(ssa_fips, columns=["ssacc", "fipsstco", "zip"])
    dfz = pd.DataFrame(zip_fips, columns=["Zipcode", "fipsstct"])
    df = MapSsaZipFips.map_city(dfs, dfz)
    assert not df.empty
    assert str(df.fipsstco.values) in str(df.fipsstct.values)


def test_map_city_bad():
    """
    Test mapping of city data via ZIP codes with bad data.
    This is tesing a dataframe merge where df_ssa "zip" merges
    with df_zip "Zipcode"
    df_merged = pd.merge(df_ssa, df_zip, how="outer", left_on="zip", right_on="Zipcode")
    """
    ssa_fips = {
        "City": [CAR1, CAR2, CAR3, CAR4],
        "xxfipsstco": [22000, 25000, 27000, 35000],
        "xxzip": [2015, 2013, 2018, 2019],
    }
    zip_fips = {"Zipcode": [2015, 2013, 2018, 2019], "fipsstct": [22000, 25000, 27000, 35000]}
    dfs = pd.DataFrame(ssa_fips, columns=["City", "xxfipsstco", "xxzip"])
    dfz = pd.DataFrame(zip_fips, columns=["Zipcode", "fipsstct"])
    df = MapSsaZipFips.map_city(dfs, dfz)
    assert df is None


def test_write_csv(tmpdir):
    """ Test writing a CSV. """
    df = _setup_df_for_test_write_csv()
    output_file_path = _setup_file_path_for_test_write_csv(tmpdir)
    MapSsaZipFips.write_csv(df, output_file_path)
    assert os.path.isfile(output_file_path)


def _setup_file_path_for_test_write_csv(tmpdir):
    project_root = Path(tmpdir)
    output_file_path = project_root.joinpath("m-test1.csv")
    with suppress(FileNotFoundError):
        os.remove(output_file_path)
    return output_file_path


def _setup_df_for_test_write_csv():
    cars = {
        "zip": [220, 250, 270, 350],
        "ssacnty": [22, 25, 27, 35],
        "countyname": [2, 3, 4, 5],
        "county": [220, 250, 270, 350],
        "stabbr": [22, 25, 27, 35],
        "statecd": [2, 3, 4, 5],
        "state": [220, 250, 270, 350],
        "city": [22, 25, 27, 35],
        "fipscc": [2, 3, 4, 5],
        "fipsstco": [22, 25, 27, 35],
        "fipsstct": [2, 3, 4, 5],
        "ssastco": [12, 13, 14, 15],
    }
    df = pd.DataFrame(
        cars,
        columns=[
            "zip",
            "ssacnty",
            "countyname",
            "county",
            "stabbr",
            "statecd",
            "state",
            "city",
            "fipscc",
            "fipsstco",
            "fipsstct",
            "ssastco",
        ],
    )
    return df
