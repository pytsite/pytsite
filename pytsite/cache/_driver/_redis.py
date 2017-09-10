"""PytSite Redis Cache Driver
"""
import pickle as _pickle
from typing import Any as _Any, Union as _Union, Mapping as _Mapping, List as _List
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
        """Init
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
        """Check whether an item exists in the pool
        """
        with _threading.get_shared_r_lock():
            key = self._get_fq_key(key)

            r = self._client.exists(key)

            if _dbg:
                if r:
                    _logger.debug("Pool '{}' HAS '{}'.".format(self.name, key))
                else:
                    _logger.debug("Pool '{}' DOES NOT HAVE '{}'.".format(self.name, key))

            return r

    def put(self, key: str, value: _Any, ttl: int = None) -> _Any:
        """Put an item into the pool
        """
        with _threading.get_shared_r_lock():
            key = self._get_fq_key(key)

            self._client.set(key, _pickle.dumps(value), ttl)

            if _reg.get('cache.debug'):
                _logger.debug("PUT '{}' into the pool '{}' with TTL {}.".format(key, self.name, ttl))

            return value

    def get(self, key: str) -> _Union[_Any, None]:
        """Get an item from the pool
        """
        with _threading.get_shared_r_lock():
            key = self._get_fq_key(key)

            if not self._client.exists(key):
                raise _KeyNotExist("Pool '{}' does not contain key '{}'.".format(self.name, key))

            item = _pickle.loads(self._client.get(key))

            if _reg.get('cache.debug'):
                _logger.debug("GET '{}' from pool '{}'.".format(key, self.name))

            return item

    def put_hash(self, key: str, value: _Mapping, ttl: int = None):
        """Put a hash-like item into the pool
        """
        with _threading.get_shared_r_lock():
            key = self._get_fq_key(key)

            self._client.hmset(key, {k: _pickle.dumps(v) for k, v in value.items()})

            if ttl:
                self._client.expire(key, ttl)

            if _reg.get('cache.debug'):
                _logger.debug("PUT '{}' into the pool '{}' with TTL {}.".format(key, self.name, ttl))

            return value

    def put_hash_item(self, key: str, hash_key: str, value: _Any) -> _Any:
        """Put a value into a hash-like item
        """
        with _threading.get_shared_r_lock():
            key = self._get_fq_key(key)

            self._client.hset(key, hash_key, _pickle.dumps(value))

            if _reg.get('cache.debug'):
                _logger.debug("PUT '{}' into the pool '{}'".format(key, self.name))

            return value

    def get_hash(self, key: str, hash_keys: _List[str] = None) -> _Mapping:
        with _threading.get_shared_r_lock():
            key = self._get_fq_key(key)

            if not self._client.exists(key):
                raise _KeyNotExist("Pool '{}' does not contain key '{}'.".format(self.name, key))

            if not hash_keys:
                hash_keys = [k.decode('utf-8') for k in self._client.hkeys(key)]

            k_num = 0
            r = {}
            for v in self._client.hmget(key, hash_keys):
                if v is None:
                    raise KeyError("'{}' pool's hash '{}' does not contain key '{}'"
                                   .format(self.name, key, hash_keys[k_num]))

                r[hash_keys[k_num]] = _pickle.loads(v)
                k_num += 1

            if _reg.get('cache.debug'):
                _logger.debug("GET '{}' from pool '{}'.".format(key, self.name))

            return r

    def get_hash_item(self, key: str, hash_key: str) -> _Any:
        """Get a value fo a key from a hash-like item
        """
        with _threading.get_shared_r_lock():
            key = self._get_fq_key(key)

            if not self._client.exists(key):
                raise _KeyNotExist("Pool '{}' does not contain key '{}'.".format(self.name, key))

            r = self._client.hget(key, hash_key)
            if r is None:
                raise KeyError("'{}' pool's hash '{}' does not contain key '{}'".format(self.name, key, hash_key))

            if _reg.get('cache.debug'):
                _logger.debug("GET '{}' from pool '{}'.".format(key, self.name))

            return _pickle.loads(r)

    def ttl(self, key: str) -> int:
        """Get key's expiration time
        """
        with _threading.get_shared_r_lock():
            key = self._get_fq_key(key)

            r = self._client.ttl(key)
            if r == -1:
                raise _KeyNeverExpires("Key '{}' in pool '{}' has no expiration time.".format(key, self.name))
            if r == -2:
                raise _KeyNotExist("Pool '{}' does not contain the key '{}'.".format(self.name, key))

            return r

    def rnm(self, key: str, new_key: str):
        """Rename a key
        """
        with _threading.get_shared_r_lock():
            if not self.has(key):
                raise KeyError("Item '{}' does not exist in pool '{}'.".format(key, self._name))

            self._client.rename(key, new_key)

            if _reg.get('cache.debug'):
                _logger.debug("RENAME '{}' to '{}' in the pool '{}'.".format(key, new_key, self.name))

    def rm(self, key: str):
        """Remove a single item from the pool
        """
        with _threading.get_shared_r_lock():
            key = self._get_fq_key(key)

            self._client.delete(key)

            if _reg.get('cache.debug'):
                _logger.debug("REMOVE '{}' from the pool '{}'.".format(key, self.name))

    def clear(self):
        """Clear entire pool
        """
        with _threading.get_shared_r_lock():
            for key in self._client.keys(_server_name + ':' + self._name + ':*'):
                self._client.delete(key)

            if _reg.get('cache.debug'):
                _logger.debug("Pool '{}' CLEARED.".format(self.name))

    def cleanup(self):
        """Cleanup outdated items from the cache
        """
        # Do nothing. Redis maintains garbage collection by itself
        if _reg.get('cache.debug'):
            _logger.debug("Pool '{}' CLEANED UP.".format(self.name))
