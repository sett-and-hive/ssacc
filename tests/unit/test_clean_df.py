""" Test CleanDF."""
import pandas as pd

from ssacc.clean_df import CleanDF

# pylint: disable=duplicate-code
# pylint: disable=R0801
# Tests do not need to be DRY


def test_construction():
    """Test construction of CleanDF. Trivial."""
    assert CleanDF()


def test_titlecase_one_column():
    """Test titlecase for one column.

    The specific values in the fixture have
    meaning to the domain use of this project.
    This is a regression test for the behavior
    of the titlecase library.
    """
    names = {
        "names": [
            "DISTRICT OF COLUMBIA",
            # stimulates bug "SAINT MARY-OF-THE-WOODS",
            "SAINT MARY OF THE WOODS",
            "Avon On Strafford",
            "BIRD IN HAND",
            # stimulates bug" lac du flambeau",
            # stimulates bug" Pointe A La Hache",
            "myers AFB",
            # stimulates bug" Jones A F B",
            "mcphearson county",
            # stimulates bug" macmillin",
            "",
            None,
        ]
    }
    names_fixture = {
        "names": [
            "District of Columbia",
            # bug in titlecase() "Saint Mary-of-the-Woods",
            "Saint Mary of the Woods",
            "Avon on Strafford",
            "Bird in Hand",
            # bug in titlecase() "Lac du Flambeau",
            # bug in titlecase() "Pointe a La Hache",
            "Myers AFB",
            # bug in titlecase() "Jones A F B",
            "McPhearson County",
            # bug in titlecase() "MacMillin",
            "",
            None,
        ]
    }
    df = pd.DataFrame(names, columns=["names"])
    df_fixture = pd.DataFrame(names_fixture, columns=["names"])
    df = CleanDF.titlecase_columns(df, ["names"])
    assert df["names"][0] == "District of Columbia"
    for i in range(len(df)):
        assert df["names"][i] == df_fixture["names"][i]


def test_titlecase_columns():
    """Test titlecase for columns.

    The specific values in the fixture have
    no specific meaning to the domain use of this project.
    """
    best_sellers = {
        "titles": [
            "MAID IN WAITING",
            "MISTER AND MISSUS PENNINGTON",
            # "MR. AND MRS. PENNINGTON",
            "THE END OF DESIRE",
            "MARY'S NECK",
            "BRIGHT SKIN",
            "A MODERN HERO",
            "INVITATION TO THE WALTZ",
        ],
        "authors": [
            "JOHN MCGALSWORTHY",
            "FRANCIS BRETT YOUNG",
            "ROBERT HERRICK",
            "BOOTH TARKINGTON",
            "JULIA PETERKIN",
            "LOUIS BROMFIELD",
            "ROSAMOND LEHMANN",
        ],
    }
    best_sellers_fixture = {
        "titles": [
            "Maid in Waiting",
            "Mister and Missus Pennington",
            # bug in titlecase() "Mr. and Mrs.Pennington",
            "The End of Desire",
            "Mary's Neck",
            "Bright Skin",
            "A Modern Hero",
            "Invitation to the Waltz",
        ],
        "authors": [
            "John McGalsworthy",
            "Francis Brett Young",
            "Robert Herrick",
            "Booth Tarkington",
            "Julia Peterkin",
            "Louis Bromfield",
            "Rosamond Lehmann",
        ],
    }
    df = pd.DataFrame(best_sellers, columns=["titles", "authors"])
    df_fixture = pd.DataFrame(best_sellers_fixture, columns=["titles", "authors"])
    df = CleanDF.titlecase_columns(df, ["titles", "authors"])
    for i in range(len(df)):
        assert df["titles"][i] == df_fixture["titles"][i]
        assert df["authors"][i] == df_fixture["authors"][i]


def test_titlecase_columns_bad_column_name():
    """Test titlecase with bad column name.

    The specific values in the fixture have
    no specific meaning to the domain use of this project.
    """
    best_sellers = {
        "titles": ["MAID IN WAITING", "MISTER AND MISSUS PENNINGTON"],
        "authors": ["JOHN MCGALSWORTHY", "FRANCIS BRETT YOUNG"],
    }
    best_sellers_fixture = {
        "titles": ["Maid in Waiting", "Mister and Missus Pennington"],
        "authors": ["John McGalsworthy", "Francis Brett Young"],
    }
    df = pd.DataFrame(best_sellers, columns=["titles", "authors"])
    df_fixture = pd.DataFrame(best_sellers_fixture, columns=["titles", "authors"])
    df = CleanDF.titlecase_columns(df, ["titles", "authors", "fake_column"])
    for i in range(len(df)):
        assert df["titles"][i] == df_fixture["titles"][i]
        assert df["authors"][i] == df_fixture["authors"][i]


def test_drop_columns():
    """ Test column dropping."""
    cars = {
        "Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
        "Price": [22000, 25000, 27000, 35000],
        "Year": [2015, 2013, 2018, 2018],
    }

    df = pd.DataFrame(cars, columns=["Brand", "Price", "Year"])
    drop_list = ["Price"]
    df1 = CleanDF.drop_columns(df, drop_list)
    assert "Price" not in df1.columns
    drop_list = ["Price", "Year"]
    df = pd.DataFrame(cars, columns=["Brand", "Price", "Year"])
    df1 = CleanDF.drop_columns(df, drop_list)
    assert "Price" not in df1.columns
    assert "Year" not in df1.columns
    drop_list = ["Price", "Year", "Oranges"]
    df = pd.DataFrame(cars, columns=["Brand", "Price", "Year"])
    df1 = CleanDF.drop_columns(df, drop_list)
    assert "Price" not in df1.columns
    assert "Year" not in df1.columns


def test_drop_columns_bad_column_name():
    """ Test column droppin with bad name."""
    cars = {
        "Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
        "Price": [22000, 25000, 27000, 35000],
        "Year": [2015, 2013, 2018, 2018],
    }

    df = pd.DataFrame(cars, columns=["Brand", "Price", "Year"])
    drop_list = ["Price", "fake_column"]
    df1 = CleanDF.drop_columns(df, drop_list)
    assert "Price" not in df1.columns


def test_reorder_columns():
    """ Test column reordering."""
    cars = {
        "Brand": ["Chevrolet Bel Air", "Lotus Esprit", "Citroën 2CV", "Aston Martin DBS V-12"],
        "Price": [49995, 59950, 18650, 114000],
        "Year": [1957, 1977, 1981, 2008],
    }
    df = pd.DataFrame(cars, columns=["Brand", "Price", "Year"])
    reordered_list = ["Year", "Brand", "Price"]
    df1 = CleanDF.reorder_columns(df, reordered_list)
    for i in range(len(df1.columns)):
        assert df1.columns[i] is reordered_list[i]


def test_dropna_rows():
    """ Test empty row dropping."""
    cars = {
        "Brand": [
            "Chitty Chitty Bang Bang",
            "Chevrolet Bel Air",
            None,
            "Citroën 2CV",
            "Aston Martin DBS V-12",
        ],
        "Price": [None, 49995, 59950, 18650, 114000],
        "Year": [1964, None, 1977, 1981, 2008],
    }
    df = pd.DataFrame(cars, columns=["Brand", "Price", "Year"])
    df1 = CleanDF.dropna_rows(df, ["Brand", "Price", "Year"])
    assert "Chitty Chitty Bang Bang" not in df1.Brand.values
    assert "Chevrolet Bel Air" not in df1.Brand.values
    assert 1977 not in df1.Year.values
    assert 1981 in df1.Year.values
    assert 114000 in df.Price.values
    assert "Aston Martin DBS V-12" in df1.Brand.values


def test_dropna_rows_bad_column_name():
    """ Test empty row droppin with bad column name."""
    cars = {
        "Brand": [
            "Chitty Chitty Bang Bang",
            "Chevrolet Bel Air",
            None,
            "Citroën 2CV",
            "Aston Martin DBS V-12",
        ],
        "Price": [None, 49995, 59950, 18650, 114000],
        "Year": [1964, None, 1977, 1981, 2008],
    }
    df = pd.DataFrame(cars, columns=["Brand", "Price", "Year"])
    df1 = CleanDF.dropna_rows(df, ["Brand", "Price", "Year", "fake_column"])
    assert "Chitty Chitty Bang Bang" not in df1.Brand.values
    assert "Chevrolet Bel Air" not in df1.Brand.values
    assert 1977 not in df1.Year.values
    assert 1981 in df1.Year.values
    assert 114000 in df.Price.values
    assert "Aston Martin DBS V-12" in df1.Brand.values


def test_rename_columns():
    """ Test column renaming."""
    cars = {
        "Brand": ["Chevrolet Bel Air", "Lotus Esprit", "Citroën 2CV", "Aston Martin DBS V-12"],
        "Price": [49995, 59950, 18650, 114000],
        "Year": [1957, 1977, 1981, 2008],
        "Sign": ["Rooster", "Snake", "Rooster", "Rat"],
    }
    original_list = ["Brand", "Price", "Year"]
    df = pd.DataFrame(cars, columns=["Brand", "Price", "Year", "Sign"])
    renamed_list = ["Marque", "Cost", "Zodiac"]
    df1 = CleanDF.rename_columns(df, original_list, renamed_list)
    for i in range(len(df1.columns)):
        if i < len(original_list):
            assert df1.columns[i] is renamed_list[i]


def test_rename_columns_bad_column_name():
    """ Test column renamin with bad column name."""
    cars = {
        "Brand": ["Chevrolet Bel Air", "Lotus Esprit"],
        "Price": [49995, 59950],
        "Year": [1957, 1977],
        "Sign": ["Rooster", "Snake"],
    }
    original_list = ["Brand", "Price", "Year", "fake_column"]
    df = pd.DataFrame(cars, columns=["Brand", "Price", "Year", "Sign"])
    renamed_list = ["Marque", "Cost", "Zodiac", "bogus_column"]
    df1 = CleanDF.rename_columns(df, original_list, renamed_list)
    assert df1.columns[0] is renamed_list[0]
    assert df1.columns[1] is renamed_list[1]
    assert df1.columns[2] is renamed_list[2]
    assert df1.columns[3] is not renamed_list[3]
