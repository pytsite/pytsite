"""PytSite Abstract Cache Driver
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Any as _Any, Mapping as _Mapping, List as _List, Generator as _Generator, Optional as _Optional
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from os import path as _path, unlink as _unlink, makedirs as _makedirs, walk as _walk
from shutil import rmtree as _rmtree
from pickle import dumps as _pickle_dump, loads as _pickle_load, UnpicklingError as _UnpicklingError
from time import time as _time
from pytsite import reg as _reg, util as _util
from . import _error


class Abstract(_ABC):
    """Abstract Cache Driver
    """

    @_abstractmethod
    def keys(self, pool: str) -> _Generator[str, None, None]:
        """Get all keys of the pool
        """
        pass

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
    def get_hash_item(self, pool: str, key: str, item_key: str, default=None) -> _Any:
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
    def ttl(self, pool: str, key: str) -> _Optional[int]:
        """Get remaining time to live of a key
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
        from pytsite import router as _router

        self._server_name = _router.server_name()
        self._path = _reg.get('cache.file_driver_storage', _path.join(_reg.get('paths.storage'), 'cache'))

        # Create cache directory
        if not _path.exists(self._path):
            _makedirs(self._path, 0o755, True)

    def _get_key_path(self, pool: str, key: str) -> str:
        """Get key's file path
        """
        h = _util.md5_hex_digest(key)
        return _path.join(self._path, self._server_name, pool, h[:2], h[2:4], key.replace(_path.sep, '.'))

    def _get_key_dir(self, pool: str, key: str) -> str:
        """Get key's file directory
        """
        return _path.dirname(self._get_key_path(pool, key))

    def _load_key(self, pool: str, key) -> dict:
        """Load key from file
        """
        f_path = self._get_key_path(pool, key)

        try:
            with open(f_path, 'rb') as f:
                return _pickle_load(f.read())

        except FileNotFoundError:
            raise _error.KeyNotExist(pool, key)

        except (EOFError, _UnpicklingError):
            _unlink(f_path)
            raise _error.KeyNotExist(pool, key)

    def keys(self, pool: str) -> _Generator[str, None, None]:
        """Get all keys of the pool
        """
        for root, dirs, files in _walk(_path.join(self._path, self._server_name, pool), topdown=False):
            for name in files:
                f_path = _path.join(root, name)
                with open(f_path, 'rb') as f:
                    yield _pickle_load(f.read())['k']

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
            f.write(_pickle_dump({'k': key, 'c': now, 't': ttl, 'e': (now + ttl) if ttl else None, 'v': value}))

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
        val = self.get(pool, key)

        if not isinstance(val, dict):
            raise TypeError("Key '{}' is not hashable".format(key))

        return val

    def get_hash_item(self, pool: str, key: str, item_key: str, default=None) -> _Any:
        """Get a value from a hash
        """
        return self.get_hash(pool, key).get(item_key, default)

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

    def ttl(self, pool: str, key: str) -> _Optional[int]:
        """Get remaining time to live of a key
        """
        expires = self._load_key(pool, key)['e']

        return int(expires - _time()) if expires else None

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
        for root, dirs, files in _walk(_path.join(self._path, self._server_name, pool), topdown=False):
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
            _rmtree(_path.join(self._path, self._server_name, pool))
        except FileNotFoundError:
            pass
