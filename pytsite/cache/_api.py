"""PytSite Cache API
"""
from typing import Dict as _Dict
from pytsite import logger as _logger, reg as _reg
from . import _error
from ._driver import Abstract as _AbstractDriver
from ._pool import Pool as _Pool

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_current_driver = None  # type: _AbstractDriver
_pools = {}  # type: _Dict[str, _Pool]
_dbg = _reg.get('cache.debug')


def set_driver(driver: _AbstractDriver):
    """Register a cache driver
    """
    if not isinstance(driver, _AbstractDriver):
        raise TypeError('Instance of {} expected, got {}'.format(_AbstractDriver, type(driver)))

    global _current_driver
    _current_driver = driver


def get_driver() -> _AbstractDriver:
    """Get current driver instance
    """
    if not _current_driver:
        raise _error.NoDriverRegistered()

    return _current_driver


def has_pool(uid: str) -> bool:
    """Check whether a pool exists
    """
    return uid in _pools


def create_pool(uid: str) -> _Pool:
    """Create a new pool
    """
    if uid in _pools:
        raise _error.PoolExists(uid)

    _pools[uid] = _Pool(uid, get_driver)

    if _dbg:
        _logger.debug("POOL CREATED: {}".format(uid))

    return _pools[uid]


def get_pool(uid: str) -> _Pool:
    """Get a pool
    """
    try:
        if _dbg:
            _logger.debug("POOL GET: '{}'.".format(uid))

        return _pools[uid]

    except KeyError:
        raise _error.PoolNotExist(uid)


def cleanup():
    """Clear expired items in all pools
    """
    for pool in _pools.values():
        pool.cleanup()
