"""Utility functions."""

from pathlib import Path


def get_project_root() -> Path:
    """Consistently get the project root for any module in source tree."""
    return Path(__file__).parent.parent.parent
