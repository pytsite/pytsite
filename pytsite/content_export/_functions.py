"""Poster Functions.
"""
from pytsite import lang as _lang
from . import _driver

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_drivers = {}


def register_driver(name: str, title: str, driver_cls: type):
    """Register export driver.
    """
    if name in _drivers:
        raise KeyError("Driver with name '{}' already registered.")

    if not issubclass(driver_cls, _driver.Abstract):
        raise ValueError("Invalid driver's class.")

    _drivers[name] = (title, driver_cls)


def load_driver(name: str, **kwargs) -> _driver.Abstract:
    """Instantiate driver.
    """
    return get_driver_info(name)[1](**kwargs)


def get_driver_info(name: str) -> tuple:
    if name not in _drivers:
        raise KeyError("Driver with name '{}' is not registered.")

    return _drivers[name]


def get_drivers() -> dict:
    """Get registered drivers.
    """
    return _drivers


def get_driver_title(name) -> str:
    return _lang.t(get_driver_info(name)[0])
