"""PytSite Cache API.
"""
from typing import Dict as _Dict
from pytsite import logger as _logger, reg as _reg
from . import _driver

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_pools = {}  # type: _Dict[str, _driver.Abstract]
_dbg = _reg.get('cache.debug')


def has_pool(name: str) -> bool:
    """Check whether a pool exists.
    """
    return name in _pools


def create_pool(name: str, driver: str = None) -> _driver.Abstract:
    """Create new pool.
    """
    if name in _pools:
        raise KeyError("Cache pool '{}' already exists.".format(name))

    if driver is None:
        driver = _reg.get('cache.driver', 'redis')

    if driver == 'redis':
        drv = _driver.Redis(name)
    else:
        raise ValueError("Cache driver '{}' is not supported.".format(driver))

    _pools[name] = drv

    if _dbg:
        _logger.debug("POOL CREATED: '{}', driver: '{}'.".format(name, driver), __name__)

    return drv


def get_pool(name: str) -> _driver.Abstract:
    """Get a pool.
    """
    if name not in _pools:
        raise KeyError("Pool '{}' is not defined.".format(name))

    if _dbg:
        _logger.debug("POOL GET: '{}'.".format(name), __name__)

    return _pools[name]


def clear_pool(name: str):
    """Clear a pool.
    """
    if name not in _pools:
        raise KeyError("Pool '{}' is not defined.".format(name))

    _pools[name].clear()


def delete_pool(name: str):
    """Delete a pool.
    """
    clear_pool(name)
    del _pools[name]

    if _dbg:
        _logger.debug("POOL DELETE: '{}'.".format(name), __name__)


def cleanup_pool(name: str):
    """Clear expired items in a pool.
    """
    if _dbg:
        _logger.debug("POOL CLEANUP: {}.".format(name), __name__)

    get_pool(name).cleanup()


def cleanup_pools():
    """Clear expired items in all pools.
    """
    for name in _pools.keys():
        cleanup_pool(name)
