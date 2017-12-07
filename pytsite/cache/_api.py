"""PytSite Cache API
"""
from typing import Dict as _Dict, Type as _Type
from pytsite import logger as _logger, reg as _reg
from . import _error
from ._driver import Abstract as _AbstractDriver

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_current_driver = None  # type: _Type
_pools = {}  # type: _Dict[str, _AbstractDriver]
_dbg = _reg.get('cache.debug')


def set_driver(cls: _Type):
    """Register a cache driver
    """
    if not isinstance(cls, type):
        raise TypeError('{} expected, got {}'.format(_AbstractDriver, type(cls)))

    if not issubclass(cls, _AbstractDriver):
        raise TypeError('{} expected, got {}'.format(_AbstractDriver, type(cls)))

    global _current_driver
    _current_driver = cls


def has_pool(uid: str) -> bool:
    """Check whether a pool exists
    """
    return uid in _pools


def create_pool(uid: str) -> _AbstractDriver:
    """Create a new pool
    """
    if not _current_driver:
        raise _error.NoDriverRegistered()

    if uid in _pools:
        raise _error.PoolExists("Cache pool '{}' is already exists".format(uid))

    _pools[uid] = _current_driver(uid)

    if _dbg:
        _logger.debug("POOL CREATED: '{}', driver: '{}'.".format(uid, _current_driver))

    return _pools[uid]


def get_pool(uid: str) -> _AbstractDriver:
    """Get a pool
    """
    if uid not in _pools:
        raise _error.PoolNotExist("Pool '{}' does not exist.".format(uid))

    if _dbg:
        _logger.debug("POOL GET: '{}'.".format(uid))

    return _pools[uid]


def clear_pool(uid: str):
    """Clear a pool
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
    """Clear expired items in a pool
    """
    if _dbg:
        _logger.debug("POOL CLEANUP: {}.".format(uid))

    get_pool(uid).cleanup()


def cleanup_pools():
    """Clear expired items in all pools
    """
    for name in _pools.keys():
        cleanup_pool(name)
