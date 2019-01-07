"""PytSite Abstract Cache Driver
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Any as _Any, Mapping as _Mapping, List as _List, Generator as _Generator, Optional as _Optional, \
    Type as _Type
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
        """Check whether the pool contains the key
        """
        pass

    @_abstractmethod
    def type(self, pool: str, key: str) -> _Type:
        """Get key's value type
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
    def put_hash_item(self, pool: str, key: str, item_key: str, value: _Any, ttl: int = None) -> _Any:
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
    def list_len(self, pool: str, key: str) -> int:
        """Return the length of the list stored at key
        """
        pass

    @_abstractmethod
    def get_list(self, pool: str, key: str, start: int = 0, end: int = None) -> list:
        """Return the specified elements of the list stored at key
        """
        pass

    @_abstractmethod
    def put_list(self, pool, key: str, value: list, ttl: int = None) -> list:
        """Store a list
        """
        pass

    @_abstractmethod
    def list_l_push(self, pool: str, key: str, value: _Any, ttl: int = None) -> int:
        """Insert the value at the head of the list stored at key
        """
        pass

    @_abstractmethod
    def list_r_push(self, pool: str, key: str, value: _Any, ttl: int = None) -> int:
        """Insert the value at the tail of the list stored at key
        """
        pass

    @_abstractmethod
    def list_l_pop(self, pool: str, key: str) -> _Any:
        """Remove and return the first element of the list stored at key
        """
        pass

    @_abstractmethod
    def list_r_pop(self, pool: str, key: str) -> _Any:
        """Remove and return the last element of the list stored at key
        """
        pass

    @_abstractmethod
    def expire(self, pool: str, key: str, ttl: int) -> int:
        """Set a timeout on key
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

    def _store(self, pool: str, key: str, value: _Any, ttl: int = None) -> _Any:
        """Store an item into the pool
        """
        f_path = self._get_key_path(pool, key)
        d_path = _path.dirname(f_path)

        if not _path.exists(d_path):
            _makedirs(d_path, 0o755)

        with open(f_path, 'wb') as f:
            now = _time()
            f.write(_pickle_dump({'k': key, 'c': now, 't': ttl, 'e': (now + ttl) if ttl else None, 'v': value}))

        return value

    def _load(self, pool: str, key: str) -> dict:
        """Load an item from the pool
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

    def _load_check_type(self, pool: str, key: str, expected_type: type) -> dict:
        raw = self._load(pool, key)
        if not isinstance(raw['v'], expected_type):
            raise _error.TypeError(pool, key, raw['v'])

        return raw

    def keys(self, pool: str) -> _Generator[str, None, None]:
        """Get all keys of the pool
        """
        for root, dirs, files in _walk(_path.join(self._path, self._server_name, pool), topdown=False):
            for name in files:
                f_path = _path.join(root, name)
                with open(f_path, 'rb') as f:
                    yield _pickle_load(f.read())['k']

    def has(self, pool: str, key: str) -> bool:
        """Check whether the pool contains the key
        """
        return _path.exists(self._get_key_path(pool, key))

    def type(self, pool: str, key: str) -> _Type:
        """Get key's value type
        """
        return type(self._load(pool, key)['v'])

    def put(self, pool: str, key: str, value: _Any, ttl: int = None) -> _Any:
        """Put an item into the pool
        """
        if isinstance(value, (dict, list)):
            raise _error.TypeError(pool, key, value)

        return self._store(pool, key, value, ttl)

    def get(self, pool: str, key: str) -> _Any:
        """Get an item from the pool
        """
        value = self._load(pool, key)['v']
        if isinstance(value, (dict, list)):
            raise _error.TypeError(pool, key, value)

        return value

    def put_hash(self, pool: str, key: str, value: _Mapping, ttl: int = None) -> _Any:
        """Put a hash item into the pool
        """
        if not isinstance(value, _Mapping):
            raise _error.TypeError(pool, key, value)

        return self._store(pool, key, dict(value), ttl)

    def put_hash_item(self, pool: str, key: str, item_key: str, value: _Any, ttl: int = None) -> _Any:
        """Put a value into a hash
        """
        try:
            raw = self._load_check_type(pool, key, dict)
            val = raw['v']
            val[item_key] = value
            return self._store(pool, key, val, raw['t'])

        except _error.KeyNotExist:
            return self._store(pool, key, {item_key: value}, ttl)

    def get_hash(self, pool: str, key: str, hash_keys: _List[str] = None) -> dict:
        """Get hash
        """
        val = self._load_check_type(pool, key, dict)['v']

        return {k: v for k, v in val.items() if k in hash_keys} if hash_keys else val

    def get_hash_item(self, pool: str, key: str, item_key: str, default=None) -> _Any:
        """Get a value from a hash
        """
        return self.get_hash(pool, key).get(item_key, default)

    def rm_hash_item(self, pool: str, key: str, item_key: str) -> _Any:
        """Remove a value from a hash
        """
        raw = self._load_check_type(pool, key, dict)
        val = raw['v']

        try:
            val.pop(item_key)
        except KeyError:
            pass

        return self._store(pool, key, val, raw['t'])

    def list_len(self, pool: str, key: str) -> int:
        """Return the length of the list stored at key
        """
        return len(self._load_check_type(pool, key, list)['v'])

    def get_list(self, pool: str, key: str, start: int = 0, end: int = None) -> list:
        """Return the specified elements of the list stored at key
        """
        return self._load_check_type(pool, key, list)['v'][start:end]

    def put_list(self, pool, key: str, value: list, ttl: int = None) -> list:
        """Store a list
        """
        if not isinstance(value, list):
            raise _error.TypeError(pool, key, value)

        return self._store(pool, key, value, ttl)

    def list_l_push(self, pool: str, key: str, value: _Any, ttl: int = None) -> int:
        """Insert the value at the head of the list stored at key
        """
        try:
            raw = self._load_check_type(pool, key, list)
            val = raw['v']
            val.insert(0, value)
            return len(self._store(pool, key, val, raw['t']))
        except _error.KeyNotExist:
            return len(self._store(pool, key, [value], ttl))

    def list_r_push(self, pool: str, key: str, value: _Any, ttl: int = None) -> int:
        """Insert the value at the tail of the list stored at key
        """
        try:
            raw = self._load_check_type(pool, key, list)
            val = raw['v']
            val.append(value)
            return len(self._store(pool, key, val, raw['t']))
        except _error.KeyNotExist:
            return len(self._store(pool, key, [value], ttl))

    def list_l_pop(self, pool: str, key: str) -> _Any:
        """Remove and return the first element of the list stored at key
        """
        raw = self._load_check_type(pool, key, list)
        val = raw['v']
        r = val.pop(0)
        self._store(pool, key, val, raw['t']) if val else self.rm(pool, key)

        return r

    def list_r_pop(self, pool: str, key: str) -> _Any:
        """Remove and return the last element of the list stored at key
        """
        raw = self._load_check_type(pool, key, list)
        val = raw['v']
        r = val.pop()
        self._store(pool, key, val, raw['t']) if val else self.rm(pool, key)

        return r

    def expire(self, pool: str, key: str, ttl: int):
        """Set a timeout on key
        """
        self._store(pool, key, self._load(pool, key)['v'], ttl)

    def ttl(self, pool: str, key: str) -> _Optional[int]:
        """Get remaining time to live of a key
        """
        expires = self._load(pool, key)['e']

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
