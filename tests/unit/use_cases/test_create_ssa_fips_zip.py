"""Test create_ssa_fips_zip use case."""

import pandas as pd

from ssacc.factories.factory import Factory, InjectionKeys
from ssacc.use_cases import create_ssa_fips_zip

# Tests do not need to be DRY
# pylint: disable=duplicate-code
# pylint: disable=R0801

# globals OK in these mocks
# pylint: disable=W0603

GET_FIPS_ZIP_DF_CALLED = False
GET_ZIP_CITY_DF_CALLED = False


def test_create_fips_zip_dataframe():
    """Test create_fips_zip_dataframe."""

    def mock_get_df():
        """Mock for gateway call to get DF from data."""
        global GET_FIPS_ZIP_DF_CALLED
        GET_FIPS_ZIP_DF_CALLED = True

    Factory.register(InjectionKeys.ZIPCOUNTY_READ, mock_get_df)
    create_ssa_fips_zip.create_fips_zip_dataframe()

    assert GET_FIPS_ZIP_DF_CALLED is True


def test_create_zip_city_dataframe():
    """Test create_zip_city_dataframe."""

    def mock_get_df():
        """Mock for gateway call to get DF from data."""
        global GET_ZIP_CITY_DF_CALLED
        GET_ZIP_CITY_DF_CALLED = True

    Factory.register(InjectionKeys.ZIPCODES_READ, mock_get_df)
    create_ssa_fips_zip.create_zip_city_dataframe()

    assert GET_ZIP_CITY_DF_CALLED is True


CAR1 = "Honda Civic"
CAR2 = "Toyota Corolla"
CAR3 = "Ford Focus"
CAR4 = "Audi A4"


def test_merge_dataframes_on_fipscounty():
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
    df = create_ssa_fips_zip.merge_dataframes_on_fipscounty(dfs, dfz)
    assert not df.empty
    assert str(df.fipsstco.values) in str(df.fipsstct.values)


def test_merge_dataframes_on_fipscounty_bad():
    """Test Map SSA to ZIP code via FIPS county code with bad data

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
    df = create_ssa_fips_zip.merge_dataframes_on_fipscounty(dfs, dfz)
    assert df is None


def test_merge_dataframes_on_zip_code():
    """Test mapping of city data via ZIP codes.

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
    df = create_ssa_fips_zip.merge_dataframes_on_zip_code(dfs, dfz)
    assert not df.empty
    assert str(df.fipsstco.values) in str(df.fipsstct.values)


def test_merge_dataframes_on_zip_code_bad():
    """Test mapping of city data via ZIP codes with bad data.

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
    df = create_ssa_fips_zip.merge_dataframes_on_zip_code(dfs, dfz)
    assert df is None


def test_create_ssa_fips_zip_csv():
    """Test create_ssa_fips_zip_csv."""
    # Mock ZIPCOUNTY_READ
    # Mock ZIPCODES_READ
    def mock_zipcounty_read():
        zip_fips = {
            "zip": [2015, 2013, 2018, 2019],
            "fipsstct": [22000, 25000, 27000, 35000],
            "statecd": ["22", "25", "27", "35"],
            "county": ["Derry", "Kilkenny", "Cork", "Clare"],
        }
        return pd.DataFrame(zip_fips, columns=["zip", "fipsstct", "statecd", "county"])

    def mock_zipcodes_read():
        zip_city = {
            "City": [CAR1, CAR2, CAR3, CAR4],
            "Lat": [22000, 25000, 27000, 35000],
            "Zipcode": [2015, 2013, 2018, 2019],
        }
        return pd.DataFrame(zip_city, columns=["City", "Lat", "Zipcode"])

    ssa_fips = {
        "ssacnty": [CAR1, CAR2, CAR3, CAR4],
        "fipsstco": [22000, 25000, 27000, 35000],
        "Year": [2015, 2013, 2018, 2019],
        "state": ["Denial", "Confusion", "perfection", "mind"],
        "countyname": ["Monmouthshire", "Cardiganshire", "Caernarfonshire", "Anglesey"],
        "ssastco": ["", "", "", ""],
        "fipscc": ["", "", "", ""],
        "stabbr": ["", "", "", ""],
    }
    dfs = pd.DataFrame(
        ssa_fips,
        columns=[
            "ssacnty",
            "fipsstco",
            "Year",
            "state",
            "countyname",
            "ssastco",
            "fipscc",
            "stabbr",
        ],
    )

    Factory.register(InjectionKeys.ZIPCOUNTY_READ, mock_zipcounty_read)
    Factory.register(InjectionKeys.ZIPCODES_READ, mock_zipcodes_read)

    filepath, df = create_ssa_fips_zip.create_ssa_fips_zip_csv(dfs)
    assert not df.empty
    assert filepath
    assert str(df.fipsstco.values) in str(df.fipsstct.values)
