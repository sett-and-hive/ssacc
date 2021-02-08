""" Factory to invert dependencies and support mocking in tests."""

from enum import Enum, auto
from typing import Dict


class InjectionKeys(Enum):
    """Enumerator for factory pattern for DI."""

    COUNTYRATE_SSA_FIPS_CC = auto()


class Factory:
    concrete_implementations: Dict = {}

    @classmethod
    def register(cls, key: InjectionKeys, concrete_implementation):
        cls.concrete_implementations[key] = concrete_implementation

    @classmethod
    def get(cls, key: InjectionKeys):
        return cls.concrete_implementations[key]
