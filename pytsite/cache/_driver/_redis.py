"""PytSite Redis Cache Driver
"""
import pickle as _pickle
from typing import Any as _Any, Union as _Union
from redis import StrictRedis as _StrictRedis
from pytsite import reg as _reg, logger as _logger, threading as _threading, router as _router
from ._abstract import Abstract as _Abstract
from .._error import KeyNotExist as _KeyNotExist, KeyNeverExpires as _KeyNeverExpires

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_server_name = _router.server_name()
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
        """Get fully qualified pool key.
        """
        return _server_name + ':' + self._name + ':' + key

    def has(self, key: str) -> bool:
        """Check whether an item exists in the pool.
        """
        try:
            _threading.get_shared_r_lock().acquire()

            r = self._client.exists(self._get_fq_key(key))

            if _dbg:
                if r:
                    _logger.debug("Pool '{}' HAS '{}'.".format(self.name, key))
                else:
                    _logger.debug("Pool '{}' DOES NOT HAVE '{}'.".format(self.name, key))

            return r

        finally:
            _threading.get_shared_r_lock().release()

    def get(self, key: str) -> _Union[_Any, None]:
        """Get an item from the pool.
        """
        try:
            _threading.get_shared_r_lock().acquire()

            if not self._client.exists(self._get_fq_key(key)):
                raise _KeyNotExist("Pool '{}' does not contain key '{}'.".format(self.name, key))

            item = _pickle.loads(self._client.get(self._get_fq_key(key)))

            if _reg.get('cache.debug'):
                _logger.debug("GET '{}' from pool '{}'.".format(key, self.name))

            return item

        finally:
            _threading.get_shared_r_lock().release()

    def put(self, key: str, value: _Any, ttl: int = None) -> _Any:
        """Put an item into the pool.
        """
        try:
            _threading.get_shared_r_lock().acquire()

            self._client.set(self._get_fq_key(key), _pickle.dumps(value), ttl)

            if _reg.get('cache.debug'):
                _logger.debug("PUT '{}' into the pool '{}' with TTL {}.".format(key, self.name, ttl))

            return value

        finally:
            _threading.get_shared_r_lock().release()

    def ttl(self, key: str) -> int:
        """Get key's expiration time.
        """
        try:
            _threading.get_shared_r_lock().acquire()

            r = self._client.ttl(self._get_fq_key(key))
            if r == -1:
                raise _KeyNeverExpires("Key '{}' in pool '{}' has no expiration time.".format(key, self.name))
            if r == -2:
                raise _KeyNotExist("Pool '{}' does not contain the key '{}'.".format(self.name, key))

            return r

        finally:
            _threading.get_shared_r_lock().release()

    def rnm(self, key: str, new_key: str):
        """Rename a key.
        """
        try:
            _threading.get_shared_r_lock().acquire()

            if not self.has(key):
                raise KeyError("Item '{}' does not exist in pool '{}'.".format(key, self._name))

            self._client.rename(key, new_key)

            if _reg.get('cache.debug'):
                _logger.debug("RENAME '{}' to '{}' in the pool '{}'.".format(key, new_key, self.name))

        finally:
            _threading.get_shared_r_lock().release()

    def rm(self, key: str):
        """Remove a single item from the pool.
        """
        try:
            _threading.get_shared_r_lock().acquire()

            self._client.delete(self._get_fq_key(key))

            if _reg.get('cache.debug'):
                _logger.debug("REMOVE '{}' from the pool '{}'.".format(key, self.name))

        finally:
            _threading.get_shared_r_lock().release()

    def clear(self):
        """Clear entire pool.
        """
        try:
            _threading.get_shared_r_lock().acquire()

            for key in self._client.keys(_server_name + ':' + self._name + ':*'):
                self._client.delete(key)

            if _reg.get('cache.debug'):
                _logger.debug("Pool '{}' CLEARED.".format(self.name))

        finally:
            _threading.get_shared_r_lock().release()

    def cleanup(self):
        """Cleanup outdated items from the cache.
        """
        # Do nothing. Redis maintains garbage collection by itself

        if _reg.get('cache.debug'):
            _logger.debug("Pool '{}' CLEANED UP.".format(self.name))
