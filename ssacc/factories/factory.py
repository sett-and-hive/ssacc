"""Factory to invert dependencies and support mocking in tests."""

from enum import Enum, auto
from typing import Dict


class InjectionKeys(Enum):

    """Enumerator class for factory pattern for DI."""

    COUNTYRATE_SSA_FIPS_CC = (auto(),)
    COUNTYRATE_FILEPATH = auto()


class Factory:

    """The factory class for dependency injection (DI)."""

    concrete_implementations: Dict = {}

    @classmethod
    def register(cls, key: InjectionKeys, concrete_implementation):
        """Caller can register a concrete implementation for DI."""
        cls.concrete_implementations[key] = concrete_implementation

    @classmethod
    def get(cls, key: InjectionKeys):
        """Caller can get a concrete implementation for DI."""
        return cls.concrete_implementations[key]
