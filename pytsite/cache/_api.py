"""PytSite Cache API.
"""
from typing import Dict as _Dict
from pytsite import threading as _threading, logger as _logger, reg as _reg
from . import _driver

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


__pools = {}  # type: _Dict[str, _driver.Abstract]


def has_pool(name: str) -> bool:
    with _threading.get_r_lock():
        return name in __pools


def create_pool(name: str, driver: str='memory', default_ttl: int=3600) -> _driver.Abstract:
    with _threading.get_r_lock():
        if name in __pools:
            raise KeyError("Cache pool '{}' already exists.".format(name))

        if driver == 'memory':
            drv = _driver.Memory(name, default_ttl)
        else:
            raise ValueError("Cache driver '{}' is not supported.".format(driver))

        __pools[name] = drv

        if _reg.get('cache.debug'):
            _logger.debug("New POOL CREATED: '{}', driver: '{}'.".format(name, driver), __name__)

        return drv


def get_pool(name: str) -> _driver.Abstract:
    with _threading.get_r_lock():
        if name not in __pools:
            raise KeyError("Pool '{}' is not defined.".format(name))

        return __pools[name]


def delete_pool(name: str):
    with _threading.get_r_lock():
        if name not in __pools:
            raise KeyError("Pool '{}' is not defined.".format(name))

        del __pools[name]

        if _reg.get('cache.debug'):
            _logger.debug("POOL DELETED: '{}'.".format(name), __name__)


def cleanup_pool(name: str):
    with _threading.get_r_lock():
        if _reg.get('cache.debug'):
            _logger.debug("Cache cleanup started for pool '{}'.".format(name), __name__)

        get_pool(name).cleanup()

        if _reg.get('cache.debug'):
            _logger.debug("Cache cleanup finished for pool '{}'.".format(name), __name__)


def cleanup_pools():
    for name in __pools.keys():
        cleanup_pool(name)