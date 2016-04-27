"""Poster Functions.
"""
from frozendict import frozendict as _frozendict
from . import _driver, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_drivers = {}


def register_driver(driver: _driver.Abstract):
    """Register export driver.
    """
    name = driver.get_name()

    if name in _drivers:
        raise KeyError("Driver with name '{}' already registered.")

    _drivers[name] = driver


def get_driver(name: str) -> _driver.Abstract:
    """Get driver instance.
    """
    if name not in _drivers:
        raise _error.DriverNotRegistered("Driver with name '{}' is not registered.")

    return _drivers[name]


def get_drivers() -> _frozendict:
    """Get registered drivers.
    """
    return _frozendict(_drivers)
