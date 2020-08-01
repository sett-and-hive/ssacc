# import pandas as pd
from pathlib import Path
from datatest import validate
from ssacc.validate_map import ValidateMap


def test_construction():
    assert ValidateMap()
