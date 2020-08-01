# import pandas as pd
from pathlib import Path
from datatest import validate
from ssacc.map_ssa_zip_fips import MapSsaZipFips


def test_construction():
    assert MapSsaZipFips()
