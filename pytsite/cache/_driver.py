"""PytSite Cache Drivers.
"""
from typing import Any as _Any
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from datetime import datetime as _datetime, timedelta as _timedelta
from pytsite import reg as _reg, logger as _logger, threading as _threading

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Abstract(_ABC):
    """Abstract Cache Driver.
    """
    def __init__(self, name: str, default_ttl: int=3600):
        """Init.
        """
        self._name = name
        self._ttl = default_ttl

    @property
    def name(self) -> str:
        """Get pool's name.
        """
        return self._name

    @property
    def ttl(self) -> int:
        """Get pool's TTL.
        """
        return self._ttl

    @_abstractmethod
    def has(self, key: str):
        """Check whether an item in the pool and it still alive.
        """
        pass

    @_abstractmethod
    def get(self, key: str):
        """Get an item from the pool.
        """
        pass

    @_abstractmethod
    def put(self, key: str, value: _Any, ttl: int=None):
        """Put an item into the pool.
        """
        pass

    @_abstractmethod
    def rm(self, key: str):
        """Remove a single item from the pool.
        """
        pass

    @_abstractmethod
    def reset(self):
        """Clear entire pool.
        """
        pass

    @_abstractmethod
    def cleanup(self):
        """Cleanup outdated items from the cache.
        """
        pass


class Memory(Abstract):
    def __init__(self, name: str, default_ttl: int=3600):
        """Init.
        """
        super().__init__(name, default_ttl)
        self._storage = {}

    def has(self, key: str) -> bool:
        """Check whether an item in the pool and it still alive.
        """
        with _threading.get_r_lock():
            return key in self._storage and self._storage[key][1] > _datetime.now()

    def get(self, key: str) -> _Any:
        """Get an item from the pool.
        """
        with _threading.get_r_lock():
            item = self._storage.get(key)
            if item and item[1] > _datetime.now():
                if _reg.get('cache.debug'):
                    _logger.debug("GET item '{}' from pool '{}'.".format(key, self.name), __name__)

                return item[0]

    def put(self, key: str, value: _Any, ttl: int=None):
        """Put an item into the pool.
        """
        with _threading.get_r_lock():
            if not ttl:
                ttl = self._ttl

            self._storage[key] = (value, _datetime.now() + _timedelta(seconds=ttl))

            if _reg.get('cache.debug'):
                _logger.debug("PUT item '{}' into the pool '{}' with TTL {}.".format(key, self.name, ttl), __name__)

    def rm(self, key: str):
        """Remove a single item from the pool.
        """
        with _threading.get_r_lock():
            if key in self._storage:
                del self._storage[key]

                if _reg.get('cache.debug'):
                    _logger.debug("REMOVE item '{}' from the '{}'.".format(key, self.name), __name__)

    def reset(self):
        """Clear entire pool.
        """
        with _threading.get_r_lock():
            self._storage = {}

            if _reg.get('cache.debug'):
                _logger.debug("Pool '{}' cleared.".format(self.name), __name__)

    def cleanup(self):
        """Cleanup outdated items from the cache.
        """
        with _threading.get_r_lock():
            if _reg.get('cache.debug'):
                _logger.debug("Cache cleanup started for pool '{}'.".format(self.name), __name__)

            now = _datetime.now()
            keys_to_rm = []
            for key, item in self._storage.items():
                if item[1] <= now:
                    keys_to_rm.append(key)

            for k in keys_to_rm:
                self.rm(k)

            if _reg.get('cache.debug'):
                _logger.debug("Cache cleanup finished for pool '{}'.".format(self.name), __name__)
