"""PytSite Redis Cache Driver
"""
import pickle as _pickle
from typing import Any as _Any, Union as _Union
from redis import StrictRedis as _StrictRedis
from pytsite import reg as _reg, logger as _logger
from ._abstract import Abstract as _Abstract

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_server_name = _reg.get('server.name')
_dbg = _reg.get('cache.debug')


class Redis(_Abstract):
    """Redis Cache Driver.
    """

    def __init__(self, name: str):
        """Init.
        """
        super().__init__(name)

        self._host = _reg.get('redis.host', 'localhost')
        self._port = _reg.get('redis.port', 6379)
        self._client = _StrictRedis(self._host, self._port)

    def _get_fq_key(self, key: str) -> str:
        """
        """
        return _server_name + ':' + self._name + ':' + key

    def has(self, key: str) -> bool:
        """Check whether an item is in the pool.
        """
        r = self._client.exists(self._get_fq_key(key))

        if _dbg:
            if r:
                _logger.debug("Pool '{}' HAS '{}'.".format(self.name, key), __name__)
            else:
                _logger.debug("Pool '{}' DOES NOT HAVE '{}'.".format(self.name, key), __name__)

        return r

    def get(self, key: str) -> _Union[_Any, None]:
        """Get an item from the pool.
        """
        item = self._client.get(self._get_fq_key(key))

        if item is not None:
            item = _pickle.loads(item)
            if _reg.get('cache.debug'):
                _logger.debug("GET '{}' from pool '{}'.".format(key, self.name), __name__)

        return item

    def put(self, key: str, value: _Any, ttl: int = None) -> _Any:
        """Put an item into the pool.
        """
        self._client.set(self._get_fq_key(key), _pickle.dumps(value), ttl)

        if _reg.get('cache.debug'):
            _logger.debug("PUT '{}' into the pool '{}' with TTL {}.".format(key, self.name, ttl), __name__)

        return value

    def rnm(self, key: str, new_key: str):
        """Rename a key.
        """
        if not self.has(key):
            raise KeyError("Item '{}' does not exist in pool '{}'.".format(key, self._name))

        self._client.rename(key, new_key)

        if _reg.get('cache.debug'):
            _logger.debug("RENAME '{}' to '{}' in the pool '{}'.".format(key, new_key, self.name), __name__)

    def rm(self, key: str):
        """Remove a single item from the pool.
        """
        self._client.delete(self._get_fq_key(key))

        if _reg.get('cache.debug'):
            _logger.debug("REMOVE '{}' from the pool '{}'.".format(key, self.name), __name__)

    def clear(self):
        """Clear entire pool.
        """
        for key in self._client.keys(_server_name + ':' + self._name + ':*'):
            self._client.delete(key)

        if _reg.get('cache.debug'):
            _logger.debug("Pool '{}' CLEARED.".format(self.name), __name__)

    def cleanup(self):
        """Cleanup outdated items from the cache.
        """
        # Do nothing. Redis maintains garbage collection by itself

        if _reg.get('cache.debug'):
            _logger.debug("Pool '{}' CLEANED UP.".format(self.name), __name__)
