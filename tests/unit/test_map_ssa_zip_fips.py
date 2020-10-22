"""Test MapSsaZipFips."""
import pandas as pd

from ssacc.map_ssa_zip_fips import MapSsaZipFips

# pylint: disable=duplicate-code
# pylint: disable=R0801
# Tests do not need to be DRY


def test_construction():
    """ Test the constructor. Trivial."""
    assert MapSsaZipFips()


def test_map_ssa_zip():
    """ Test Map SSA to ZIP code via FIPS county code."""
    # pd.merge(dfs, dfz, how="outer", left_on="fipsstco", right_on="fipsstct")
    ssa_fips = {
        "ssacc": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
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
    """ Test Map SSA to ZIP code via FIPS county code. with bad data"""
    # pd.merge(dfs, dfz, how="outer", left_on="fipsstco", right_on="fipsstct")
    ssa_fips = {
        "ssacc": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
        "xxfipsstco": [22000, 25000, 27000, 35000],
        "Year": [2015, 2013, 2018, 2019],
    }
    zip_fips = {"zipcode": [2015, 2013, 2018, 2019], "fipsstct": [22000, 25000, 27000, 35000]}
    dfs = pd.DataFrame(ssa_fips, columns=["ssacc", "xxfipsstco", "Year"])
    dfz = pd.DataFrame(zip_fips, columns=["zipcode", "fipsstct"])
    df = MapSsaZipFips.map_ssa_zip(dfs, dfz)
    assert df is None


def test_map_city():
    """ Test mapping of city data via ZIP codes."""
    # dfm = pd.merge(dfs, dfz, how="outer", left_on="zip", right_on="Zipcode")
    ssa_fips = {
        "City": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
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
    """ Test mapping of city data via ZIP codes with bad data."""
    # dfm = pd.merge(dfs, dfz, how="outer", left_on="zip", right_on="Zipcode")
    ssa_fips = {
        "City": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
        "xxfipsstco": [22000, 25000, 27000, 35000],
        "xxzip": [2015, 2013, 2018, 2019],
    }
    zip_fips = {"Zipcode": [2015, 2013, 2018, 2019], "fipsstct": [22000, 25000, 27000, 35000]}
    dfs = pd.DataFrame(ssa_fips, columns=["City", "xxfipsstco", "xxzip"])
    dfz = pd.DataFrame(zip_fips, columns=["Zipcode", "fipsstct"])
    df = MapSsaZipFips.map_city(dfs, dfz)
    assert df is None
