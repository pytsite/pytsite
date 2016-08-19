"""PytSite Registry Functions.
"""
from .driver import Abstract as _RegistryDriver, Memory as _MemoryDriver

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Default driver
_current_driver = _MemoryDriver()


def set_driver(driver: _RegistryDriver):
    """Switch registry driver.
    """
    global _current_driver
    _current_driver = driver


def put(key: str, value):
    """Set registry's value.
    """
    _current_driver.put(key, value)


def get(key: str, default=None):
    """Get registry's value.
    """
    return _current_driver.get(key, default)


def get_all() -> dict:
    """Get all registry's content.
    """
    return _current_driver.get_all()


def merge(other: dict):
    _current_driver.merge(other)
