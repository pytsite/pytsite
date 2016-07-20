"""PytSite Cache API.
"""
from typing import Dict as _Dict
from pytsite import logger as _logger, reg as _reg
from . import _driver, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_pools = {}  # type: _Dict[str, _driver.Abstract]
_dbg = _reg.get('cache.debug')


def has_pool(uid: str) -> bool:
    """Check whether a pool exists.
    """
    return uid in _pools


def create_pool(uid: str, driver: str = None) -> _driver.Abstract:
    """Create new pool.
    """
    if uid in _pools:
        raise _error.PoolExists("Cache pool '{}' already exists.".format(uid))

    if driver is None:
        driver = _reg.get('cache.driver', 'redis')

    if driver == 'redis':
        drv = _driver.Redis(uid)
    else:
        raise _error.DriverNotFound("Cache driver '{}' is not supported.".format(driver))

    _pools[uid] = drv

    if _dbg:
        _logger.debug("POOL CREATED: '{}', driver: '{}'.".format(uid, driver))

    return drv


def get_pool(uid: str) -> _driver.Abstract:
    """Get a pool.
    """
    if uid not in _pools:
        raise _error.PoolNotExist("Pool '{}' does not exist.".format(uid))

    if _dbg:
        _logger.debug("POOL GET: '{}'.".format(uid))

    return _pools[uid]


def clear_pool(uid: str):
    """Clear a pool.
    """
    if uid not in _pools:
        raise KeyError("Pool '{}' is not defined.".format(uid))

    _pools[uid].clear()


def delete_pool(uid: str):
    """Delete a pool.
    """
    clear_pool(uid)
    del _pools[uid]

    if _dbg:
        _logger.debug("POOL DELETE: '{}'.".format(uid))


def cleanup_pool(uid: str):
    """Clear expired items in a pool.
    """
    if _dbg:
        _logger.debug("POOL CLEANUP: {}.".format(uid))

    get_pool(uid).cleanup()


def cleanup_pools():
    """Clear expired items in all pools.
    """
    for name in _pools.keys():
        cleanup_pool(name)
