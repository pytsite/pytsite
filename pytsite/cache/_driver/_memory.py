"""PytSite Memory Cache Driver
"""
from typing import Any as _Any, Union as _Union
from datetime import datetime as _datetime, timedelta as _timedelta
from pytsite import reg as _reg, logger as _logger
from ._abstract import Abstract as _Abstract

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_dbg = _reg.get('cache.debug')


class Memory(_Abstract):
    def __init__(self, name: str):
        """Init.
        """
        super().__init__(name)
        self._storage = {}

    def has(self, key: str) -> bool:
        """Check whether an item in the pool.
        """
        r = key in self._storage and self._storage[key][1] > _datetime.now()

        if _dbg:
            if r:
                _logger.debug("Pool '{}' HAS '{}'.".format(self.name, key), __name__)
            else:
                _logger.debug("Pool '{}' DOES NOT HAVE '{}'.".format(self.name, key), __name__)

        return r

    def get(self, key: str) -> _Union[_Any, None]:
        """Get an item from the pool.
        """
        item = self._storage.get(key)
        if item and item[1] is not None and item[1] > _datetime.now():
            if _dbg:
                _logger.debug("GET '{}' from the pool '{}'.".format(key, self.name), __name__)

            return item[0]

    def put(self, key: str, value: _Any, ttl: int = None) -> _Any:
        """Put an item into the pool.
        """
        self._storage[key] = (value, _datetime.now() + _timedelta(seconds=ttl))

        if _reg.get('cache.debug'):
            _logger.debug("PUT '{}' into the pool '{}' with TTL {}.".format(key, self.name, ttl), __name__)

        return value

    def rnm(self, key: str, new_key: str):
        """Rename a key.
        """
        if key not in self._storage:
            raise KeyError("Item '{}' does not exist in pool '{}'.".format(key, self._name))

        self._storage[new_key] = self._storage.pop(key)

        if _reg.get('cache.debug'):
            _logger.debug("RENAME '{}' to '{}' in the pool '{}'.".format(key, new_key, self.name), __name__)

    def rm(self, key: str):
        """Remove a single item from the pool.
        """
        if key in self._storage:
            del self._storage[key]

            if _reg.get('cache.debug'):
                _logger.debug("REMOVE '{}' from the pool '{}'.".format(key, self.name), __name__)

    def clear(self):
        """Clear entire pool.
        """
        self._storage = {}

        if _reg.get('cache.debug'):
            _logger.debug("Pool '{}' CLEARED.".format(self.name), __name__)

    def cleanup(self):
        """Cleanup outdated items from the cache.
        """
        now = _datetime.now()
        keys_to_rm = []
        for key, item in self._storage.items():
            if item[1] is not None and item[1] <= now:
                keys_to_rm.append(key)

        deleted_n = 0
        for k in keys_to_rm:
            self.rm(k)
            deleted_n += 1

        if _reg.get('cache.debug'):
            _logger.debug("Pool '{}' CLEANED UP. Removed {} items.".format(self.name, deleted_n), __name__)
