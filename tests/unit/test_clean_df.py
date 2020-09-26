import pandas as pd

from ssacc.clean_df import CleanDF


def test_construction():
    assert CleanDF()


def test_titlecase_column():
    cd = CleanDF()
    names = {
        "names": [
            "DISTRICT OF COLUMBIA",
            # "SAINT MARY-OF-THE-WOODS",
            "SAINT MARY OF THE WOODS",
            "Avon On Strafford",
            "BIRD IN HAND",
            # "lac du flambeau",
            # "Pointe A La Hache",
            "myers AFB",
            # "Jones A F B",
            "mcphearson county",
            # "macmillin",
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
    df = cd.titlecase_column(df, "names")
    assert df["names"][0] == "District of Columbia"
    for i in range(len(df)):
        assert df["names"][i] == df_fixture["names"][i]
