""" Factory to invert dependency from volume conversion to conversion gateway."""

from enum import Enum, auto


class InjectionKeys(Enum):
    PLACEHOLDER = auto()
