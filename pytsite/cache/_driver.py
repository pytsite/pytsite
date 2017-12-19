"""PytSite Abstract Cache Driver
"""
from typing import Any as _Any, Mapping as _Mapping, List as _List
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from os import path as _path, unlink as _unlink, makedirs as _makedirs, walk as _walk
from shutil import rmtree as _rmtree
from pickle import dumps as _pickle_dump, loads as _pickle_load
from time import time as _time
from pytsite import reg as _reg, util as _util, router as _router
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_server_name = _router.server_name()


class Abstract(_ABC):
    """Abstract Cache Driver
    """

    @_abstractmethod
    def has(self, pool: str, key: str) -> bool:
        """Check whether an item exists in the pool
        """
        pass

    @_abstractmethod
    def put(self, pool: str, key: str, value: _Any, ttl: int = None) -> _Any:
        """Put an item into the pool
        """
        pass

    @_abstractmethod
    def get(self, pool: str, key: str) -> _Any:
        """Get an item from the pool
        """
        pass

    @_abstractmethod
    def put_hash(self, pool: str, key: str, value: _Mapping, ttl: int = None) -> _Any:
        """Put a hash item into the pool
        """
        pass

    @_abstractmethod
    def put_hash_item(self, pool: str, key: str, item_key: str, value: _Any) -> _Any:
        """Put a value into a hash
        """
        pass

    @_abstractmethod
    def get_hash(self, pool: str, key: str, hash_keys: _List[str] = None) -> _Mapping:
        """Get hash
        """
        pass

    @_abstractmethod
    def get_hash_item(self, pool: str, key: str, item_key: str) -> _Any:
        """Get a value from a hash
        """
        pass

    @_abstractmethod
    def rm_hash_item(self, pool: str, key: str, item_key: str) -> _Any:
        """Remove a value from a hash
        """
        pass

    @_abstractmethod
    def l_push(self, pool: str, key: str, value: _Any) -> int:
        """Push a value into beginning of a list
        """
        pass

    @_abstractmethod
    def r_pop(self, pool: str, key: str) -> _Any:
        """Pop an item from the end of a list
        """
        pass

    @_abstractmethod
    def ttl(self, pool: str, key: str) -> int:
        """Get key's expiration time
        """
        pass

    @_abstractmethod
    def rnm(self, pool: str, key: str, new_key: str):
        """Rename a key
        """
        pass

    @_abstractmethod
    def rm(self, pool: str, key: str):
        """Remove a value from the pool
        """
        pass

    @_abstractmethod
    def cleanup(self, pool: str):
        """Cleanup outdated items from the pool
        """
        pass

    @_abstractmethod
    def clear(self, pool: str):
        """Clear entire pool
        """
        pass


class File(Abstract):
    """PytSite Filesystem Based Cache
    """

    def __init__(self):
        """Init
        """
        self._path = _reg.get('cache.file_driver_storage', _path.join(_reg.get('paths.tmp'), 'cache'))

    def _get_key_path(self, pool: str, key: str) -> str:
        h = _util.md5_hex_digest(key)

        return _path.join(self._path, _server_name, pool, h[:2], h[2:4], key)

    def _get_key_dir(self, pool: str, key: str) -> str:
        return _path.dirname(self._get_key_path(pool, key))

    def _load_key(self, pool: str, key) -> dict:
        try:
            with open(self._get_key_path(pool, key), 'rb') as f:
                return _pickle_load(f.read())

        except FileNotFoundError:
            raise _error.KeyNotExist(pool, key)

    def has(self, pool: str, key: str) -> bool:
        """Check whether an item exists in the pool
        """
        return _path.exists(self._get_key_path(pool, key))

    def put(self, pool: str, key: str, value: _Any, ttl: int = None) -> _Any:
        """Put an item into the pool
        """
        f_path = self._get_key_path(pool, key)
        d_path = _path.dirname(f_path)

        if not _path.exists(d_path):
            _makedirs(d_path, 0o755)

        with open(f_path, 'wb') as f:
            now = _time()
            f.write(_pickle_dump({'c': now, 't': ttl, 'e': (now + ttl) if ttl else None, 'v': value}))

        return value

    def get(self, pool: str, key: str) -> _Any:
        """Get an item from the pool
        """
        return self._load_key(pool, key)['v']

    def put_hash(self, pool: str, key: str, value: _Mapping, ttl: int = None) -> _Any:
        """Put a hash item into the pool
        """
        if not isinstance(value, _Mapping):
            raise TypeError('{} expected, got {}'.format(_Mapping.__class__, type(value)))

        return self.put(pool, key, dict(value), ttl)

    def put_hash_item(self, pool: str, key: str, item_key: str, value: _Any) -> _Any:
        """Put a value into a hash
        """
        raw = self._load_key(pool, key)
        val = raw['v']
        if not isinstance(val, dict):
            raise TypeError("Key '{}' is not hashable".format(key))

        val[item_key] = value

        return self.put(pool, key, val, raw['t'])

    def get_hash(self, pool: str, key: str, hash_keys: _List[str] = None) -> _Mapping:
        """Get hash
        """
        raise NotImplementedError()

    def get_hash_item(self, pool: str, key: str, item_key: str) -> _Any:
        """Get a value from a hash
        """
        val = self.get(pool, key)

        if not isinstance(val, dict):
            raise TypeError("Key '{}' is not hashable".format(key))

        return val.get(item_key)

    def rm_hash_item(self, pool: str, key: str, item_key: str) -> _Any:
        """Remove a value from a hash
        """
        raw = self._load_key(pool, key)
        val = raw['v']
        if not isinstance(val, dict):
            raise TypeError("Key '{}' is not hashable".format(key))

        try:
            val.pop(item_key)
        except KeyError:
            pass

        return self.put(pool, key, val, raw['t'])

    def l_push(self, pool: str, key: str, value: _Any) -> int:
        """Push a value into beginning of a list
        """
        try:
            val = self.get(pool, key)
            if not isinstance(val, list):
                raise TypeError("Value of the key '{}' is not a list: {}".format(key, val))
            val.insert(0, value)
            self.put(pool, key, val)

            return len(val)

        except _error.KeyNotExist:
            val = list()
            val.append(value)
            self.put(pool, key, val)

            return 1

    def r_pop(self, pool: str, key: str) -> _Any:
        """Pop an item from the end of a list
        """
        val = self.get(pool, key)
        if not isinstance(val, list):
            raise TypeError("Value of the key '{}' is not a list: {}".format(key, val))

        try:
            r = val.pop()
            self.put(pool, key, val)
            return r

        except IndexError:
            raise _error.KeyNotExist(pool, key)

    def ttl(self, pool: str, key: str) -> int:
        """Get key's expiration time
        """
        return self._load_key(pool, key)['t']

    def rnm(self, pool: str, key: str, new_key: str):
        """Rename a key
        """
        raise NotImplementedError()

    def rm(self, pool: str, key: str):
        """Remove a value from the pool
        """
        try:
            _unlink(self._get_key_path(pool, key))
        except FileNotFoundError:
            pass

    def cleanup(self, pool: str):
        """Cleanup outdated items from the cache
        """
        for root, dirs, files in _walk(_path.join(self._path, _server_name, pool), topdown=False):
            for name in files:
                f_path = _path.join(root, name)
                with open(f_path, 'rb') as f:
                    expires = _pickle_load(f.read())['e']

                if expires and expires <= _time():
                    try:
                        _unlink(f_path)
                    except FileNotFoundError:
                        pass

    def clear(self, pool: str):
        """Clear entire pool
        """
        try:
            _rmtree(_path.join(self._path, _server_name, pool))
        except FileNotFoundError:
            pass