"""PytSite Abstract Cache Driver
"""
from typing import Any as _Any, Mapping as _Mapping, List as _List
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from os import path as _path, unlink as _unlink, makedirs as _makedirs, walk as _walk
from shutil import rmtree as _rmtree
from pickle import dumps as _pickle_dump, loads as _pickle_load
from time import time as _time
from pytsite import reg as _reg, util as _util
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_FILE_CACHE_PATH = _path.join(_reg.get('paths.tmp'), 'cache')


class Abstract(_ABC):
    """Abstract Cache Driver
    """

    def __init__(self, pool_uid: str):
        """Init
        """
        self._pool_uid = pool_uid

    @property
    def pool_uid(self) -> str:
        """Get pool's name
        """
        return self._pool_uid

    @_abstractmethod
    def has(self, key: str) -> bool:
        """Check whether an item exists in the pool
        """
        pass

    @_abstractmethod
    def put(self, key: str, value: _Any, ttl: int = None) -> _Any:
        """Put an item into the pool
        """
        pass

    @_abstractmethod
    def get(self, key: str) -> _Any:
        """Get an item from the pool
        """
        pass

    @_abstractmethod
    def put_hash(self, key: str, value: _Mapping, ttl: int = None) -> _Any:
        """Put a hash item into the pool
        """
        pass

    @_abstractmethod
    def put_hash_item(self, key: str, item_key: str, value: _Any) -> _Any:
        """Put a value into a hash
        """
        pass

    @_abstractmethod
    def get_hash(self, key: str, hash_keys: _List[str] = None) -> _Mapping:
        """Get hash
        """
        pass

    @_abstractmethod
    def get_hash_item(self, key: str, item_key: str) -> _Any:
        """Get a value from a hash
        """
        pass

    @_abstractmethod
    def rm_hash_item(self, key: str, item_key: str) -> _Any:
        """Remove a value from a hash
        """
        pass

    @_abstractmethod
    def l_push(self, key: str, value: _Any) -> int:
        """Push a value into beginning of a list
        """
        pass

    @_abstractmethod
    def r_pop(self, key: str) -> _Any:
        """Pop an item from the end of a list
        """
        pass

    @_abstractmethod
    def ttl(self, key: str) -> int:
        """Get key's expiration time
        """
        pass

    @_abstractmethod
    def rnm(self, key: str, new_key: str):
        """Rename a key
        """
        pass

    @_abstractmethod
    def rm(self, key: str):
        """Remove a value from the pool
        """
        pass

    @_abstractmethod
    def clear(self):
        """Clear entire pool
        """
        pass

    @_abstractmethod
    def cleanup(self):
        """Cleanup outdated items from the cache
        """
        pass


class File(Abstract):
    """PytSite Filesystem Based Cache
    """

    def __init__(self, pool_uid: str):
        """Init
        """
        super().__init__(pool_uid)

        self._path = _path.join(_FILE_CACHE_PATH, pool_uid)

    def _get_key_path(self, key: str) -> str:
        h = _util.md5_hex_digest(key)

        return _path.join(_FILE_CACHE_PATH, self._pool_uid, h[:2], h[2:4], h)

    def _get_key_dir(self, key: str) -> str:
        return _path.dirname(self._get_key_path(key))

    def _load_key(self, key) -> dict:
        try:
            with open(self._get_key_path(key), 'rb') as f:
                return _pickle_load(f.read())

        except FileNotFoundError:
            raise _error.KeyNotExist(self._pool_uid, key)

    def has(self, key: str) -> bool:
        """Check whether an item exists in the pool
        """
        return _path.exists(self._get_key_path(key))

    def put(self, key: str, value: _Any, ttl: int = None) -> _Any:
        """Put an item into the pool
        """
        f_path = self._get_key_path(key)
        d_path = _path.dirname(f_path)

        if not _path.exists(d_path):
            _makedirs(d_path, 0o755)

        with open(f_path, 'wb') as f:
            now = _time()
            f.write(_pickle_dump({'c': now, 't': ttl, 'e': (now + ttl) if ttl else None, 'v': value}))

        return value

    def get(self, key: str) -> _Any:
        """Get an item from the pool
        """
        return self._load_key(key)['v']

    def put_hash(self, key: str, value: _Mapping, ttl: int = None) -> _Any:
        """Put a hash item into the pool
        """
        if not isinstance(value, _Mapping):
            raise TypeError('{} expected, got {}'.format(_Mapping.__class__, type(value)))

        return self.put(key, dict(value), ttl)

    def put_hash_item(self, key: str, item_key: str, value: _Any) -> _Any:
        """Put a value into a hash
        """
        raw = self._load_key(key)
        val = raw['v']
        if not isinstance(val, dict):
            raise TypeError("Key '{}' is not hashable".format(key))

        val[item_key] = value

        return self.put(key, val, raw['t'])

    def get_hash(self, key: str, hash_keys: _List[str] = None) -> _Mapping:
        """Get hash
        """
        raise NotImplementedError()

    def get_hash_item(self, key: str, item_key: str) -> _Any:
        """Get a value from a hash
        """
        val = self.get(key)

        if not isinstance(val, dict):
            raise TypeError("Key '{}' is not hashable".format(key))

        return val.get(item_key)

    def rm_hash_item(self, key: str, item_key: str) -> _Any:
        """Remove a value from a hash
        """
        raw = self._load_key(key)
        val = raw['v']
        if not isinstance(val, dict):
            raise TypeError("Key '{}' is not hashable".format(key))

        val.pop(item_key)

        return self.put(key, val, raw['t'])

    def l_push(self, key: str, value: _Any) -> int:
        """Push a value into beginning of a list
        """
        try:
            val = self.get(key)
            if not isinstance(val, list):
                raise TypeError("Value of the key '{}' is not a list: {}".format(key, val))
            val.insert(0, value)
            self.put(key, val)

            return len(val)

        except _error.KeyNotExist:
            val = list()
            val.append(value)
            self.put(key, val)

            return 1

    def r_pop(self, key: str) -> _Any:
        """Pop an item from the end of a list
        """
        val = self.get(key)
        if not isinstance(val, list):
            raise TypeError("Value of the key '{}' is not a list: {}".format(key, val))

        try:
            r = val.pop()
            self.put(key, val)
            return r

        except IndexError:
            raise _error.KeyNotExist(self._pool_uid, key)

    def ttl(self, key: str) -> int:
        """Get key's expiration time
        """
        return self._load_key(key)['t']

    def rnm(self, key: str, new_key: str):
        """Rename a key
        """
        raise NotImplementedError()

    def rm(self, key: str):
        """Remove a value from the pool
        """
        try:
            _unlink(self._get_key_path(key))
        except FileNotFoundError:
            pass

    def clear(self):
        """Clear entire pool
        """
        _rmtree(_path.join(_FILE_CACHE_PATH, self._pool_uid))

    def cleanup(self):
        """Cleanup outdated items from the cache
        """
        for root, dirs, files in _walk(_path.join(_FILE_CACHE_PATH, self._pool_uid), topdown=False):
            for name in files:
                f_path = _path.join(root, name)
                with open(f_path, 'rb') as f:
                    expires = _pickle_load(f.read())['e']

                if expires and expires <= _time():
                    try:
                        _unlink(f_path)
                    except FileNotFoundError:
                        pass
