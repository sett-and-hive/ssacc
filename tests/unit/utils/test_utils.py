""" Test utilities."""

from pathlib import Path

from ssacc.utils import utils


def test_get_project_root():
    """ Test get_project_root."""
    # .tests/unit/utils/<this file>
    # This test is disturbingly knowin of where
    #  it lives in the source tree
    path = utils.get_project_root()
    assert path == Path(__file__).parent.parent.parent.parent
