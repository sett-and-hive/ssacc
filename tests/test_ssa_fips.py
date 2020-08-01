# import pandas as pd
from pathlib import Path

from datatest import validate

from ssacc.ssa_fips import SsaFips


def test_construction():
    assert SsaFips()

"""
def test_csv_read():
    s = SsaFips()
    project_root = Path(__file__).parents[0]
    file_path = project_root.joinpath("data", "test1.csv")
    print(file_path)
    required_columns = {"ssacounty", "rating", "year", "runtime"}
    df = s.csv_read(file_path)
    validate(df.fieldname, required_columns)
"""

"""
def test_csv_read_bad_file():
    s = Ssa_fips()
    project_root = Path(__file__).parents[0]
    file_path = project_root.joinpath("data", "test12.csv")
    required_columns = {"ssacounty", "rating", "year", "runtime"}
    df = s.csv_read(file_path)
    validate(df.columns, required_columns)
"""