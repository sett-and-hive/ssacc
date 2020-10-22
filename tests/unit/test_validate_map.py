""" Test ValidateMap."""
from ssacc.validate_map import ValidateMap

# pylint: disable=duplicate-code
# pylint: disable=R0801
# Tests do not need to be DRY


def test_construction():
    """ Test the constructor. Trivial."""
    assert ValidateMap()
