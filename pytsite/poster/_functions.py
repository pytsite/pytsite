"""Poster Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from . import _driver

__drivers = {}


def register_driver(name: str, title: str, driver_cls: type):
    """Register oAuth driver.
    """
    if name in __drivers:
        raise KeyError("Driver with name '{}' already registered.")

    if not issubclass(driver_cls, _driver.Abstract):
        raise ValueError("Invalid driver's class.")

    __drivers[name] = (title, driver_cls)


def load_driver(name: str, **kwargs) -> _driver.Abstract:
    """Instantiate driver.
    """
    if name not in __drivers:
        raise KeyError("Driver with name '{}' is not registered.")

    return __drivers[name][1](**kwargs)


def get_drivers() -> dict:
    """Get registered drivers.
    """
    return __drivers
