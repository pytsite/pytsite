"""PytSite Content Import API.
"""
from typing import Dict as _Dict
from frozendict import frozendict as _frozendict
from pytsite import lang as _lang
from . import _driver, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


__drivers = {}  # type: _Dict[str, _driver.Abstract]


def register_driver(driver: _driver.Abstract):
    """Register a content import driver.
    """
    __drivers[driver.get_name()] = driver


def get_drivers() -> _Dict[str, _driver.Abstract]:
    """Get all the registered drivers.
    """
    return _frozendict(__drivers)


def get_driver(driver_name: str) -> _driver.Abstract:
    """Get a content import driver by name.
    """
    if driver_name not in __drivers:
        raise _error.DriverNotRegistered("Content import driver '{}' is not registered.")

    return __drivers[driver_name]
