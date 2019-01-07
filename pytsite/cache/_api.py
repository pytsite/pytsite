"""PytSite Cache API
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Dict as _Dict
from pytsite import logger as _logger, reg as _reg
from . import _error
from ._driver import Abstract as _AbstractDriver
from ._pool import Pool as _Pool

_current_driver = None  # type: _AbstractDriver
_pools = {}  # type: _Dict[str, _Pool]
_dbg = _reg.get('cache.debug')


def set_driver(driver: _AbstractDriver):
    """Register a cache driver
    """
    global _current_driver

    if not isinstance(driver, _AbstractDriver):
        raise TypeError('Instance of {} expected, got {}'.format(_AbstractDriver, type(driver)))

    # When switching from one driver to another, it is important to move existing keys to the new storage
    keys_to_move = {}  # type: _Dict[str, list]
    if _current_driver:
        for pool in _pools.values():
            keys_to_move[pool.uid] = []
            for key in pool.keys():
                key_type = pool.type(key)
                if key_type in (list, tuple):
                    value = pool.get_list(key)
                elif key_type is dict:
                    value = pool.get_hash(key)
                else:
                    value = pool.get(key)

                keys_to_move[pool.uid].append((key, value, pool.ttl(key)))  # Remember key and value
                _pools[pool.uid].rm(key)  # Delete key via current driver

    # Switch to the new driver
    _current_driver = driver

    # Move keys from previous driver
    for pool_uid, keys in keys_to_move.items():
        for key, value, ttl in keys:
            # Clear previous value
            _pools[pool_uid].rm(key)

            if isinstance(value, list):
                _pools[pool_uid].put_list(key, value)
            elif isinstance(value, dict):
                _pools[pool_uid].put_hash(key, value)
            else:
                _pools[pool_uid].put(key, value, ttl)


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


def get_pools() -> _Dict[str, _Pool]:
    """Get all pools
    """
    return _pools.copy()


def cleanup():
    """Clear expired items in all pools
    """
    for pool in _pools.values():
        pool.cleanup()
