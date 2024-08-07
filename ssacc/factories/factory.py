"""Factory to invert dependencies and support mocking in tests."""

from enum import Enum, auto
from typing import Dict


class InjectionKeys(Enum):
    """Enumerator class for factory pattern for DI."""

    # Apapters
    # County rate data gateway
    COUNTYRATE_SSA_FIPS_CC = (auto(),)
    COUNTYRATE_FILEPATH = (auto(),)
    # USPS ZIP FIPS data gateway
    USPS_ZIPCTY_PATH = (auto(),)
    USPS_ZIPCTY_READ = (auto(),)
    GET_USPS_ZIP_FIPS_CC = (auto(),)
    # State code JSON data gateway
    STATE_JSON_FILEPATH = (auto(),)
    STATE_JSON_READ = (auto(),)
    GET_STATE_JSON = (auto(),)
    # zipcounty CSV data gateway
    ZIPCOUNTY_FILEPATH = (auto(),)
    ZIPCOUNTY_READ = (auto(),)
    ZIPCOUNTY_WRITE = (auto(),)
    # zipcodes CSV data gateway
    ZIPCODES_FILEPATH = (auto(),)
    ZIPCODES_READ = (auto(),)
    # SSA FIPS ZIP CSV data gateway
    SSAFIPZIPS_FILEPATH = (auto(),)


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

    @classmethod
    def reset(cls):
        """Caller can reset the factory state."""
        cls.concrete_implementations = {}
