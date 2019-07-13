"""PytSite Cache Builtin Drivers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Any, Mapping, List, Generator, Optional, Type
from abc import ABC, abstractmethod
from os import path, unlink, makedirs, walk
from shutil import rmtree
from pickle import dumps as pickle_dump, loads as pickle_load, UnpicklingError
from time import time
from pytsite import reg, util
from . import _error


class Abstract(ABC):
    """Abstract Cache Driver
    """

    @abstractmethod
    def keys(self, pool: str) -> Generator[str, None, None]:
        """Get all keys of the pool
        """
        pass

    @abstractmethod
    def has(self, pool: str, key: str) -> bool:
        """Check whether the pool contains the key
        """
        pass

    @abstractmethod
    def type(self, pool: str, key: str) -> Type:
        """Get key's value type
        """
        pass

    @abstractmethod
    def put(self, pool: str, key: str, value: Any, ttl: int = None) -> Any:
        """Put an item into the pool
        """
        pass

    @abstractmethod
    def get(self, pool: str, key: str) -> Any:
        """Get an item from the pool
        """
        pass

    @abstractmethod
    def put_hash(self, pool: str, key: str, value: Mapping, ttl: int = None) -> Any:
        """Put a hash item into the pool
        """
        pass

    @abstractmethod
    def put_hash_item(self, pool: str, key: str, item_key: str, value: Any, ttl: int = None) -> Any:
        """Put a value into a hash
        """
        pass

    @abstractmethod
    def get_hash(self, pool: str, key: str, hash_keys: List[str] = None) -> Mapping:
        """Get hash
        """
        pass

    @abstractmethod
    def get_hash_item(self, pool: str, key: str, item_key: str, default=None) -> Any:
        """Get a value from a hash
        """
        pass

    @abstractmethod
    def rm_hash_item(self, pool: str, key: str, item_key: str) -> Any:
        """Remove a value from a hash
        """
        pass

    @abstractmethod
    def list_len(self, pool: str, key: str) -> int:
        """Return the length of the list stored at key
        """
        pass

    @abstractmethod
    def get_list(self, pool: str, key: str, start: int = 0, end: int = None) -> list:
        """Return the specified elements of the list stored at key
        """
        pass

    @abstractmethod
    def put_list(self, pool, key: str, value: list, ttl: int = None) -> list:
        """Store a list
        """
        pass

    @abstractmethod
    def list_l_push(self, pool: str, key: str, value: Any, ttl: int = None) -> int:
        """Insert the value at the head of the list stored at key
        """
        pass

    @abstractmethod
    def list_r_push(self, pool: str, key: str, value: Any, ttl: int = None) -> int:
        """Insert the value at the tail of the list stored at key
        """
        pass

    @abstractmethod
    def list_l_pop(self, pool: str, key: str) -> Any:
        """Remove and return the first element of the list stored at key
        """
        pass

    @abstractmethod
    def list_r_pop(self, pool: str, key: str) -> Any:
        """Remove and return the last element of the list stored at key
        """
        pass

    @abstractmethod
    def expire(self, pool: str, key: str, ttl: int) -> int:
        """Set a timeout on key
        """
        pass

    @abstractmethod
    def ttl(self, pool: str, key: str) -> Optional[int]:
        """Get remaining time to live of a key
        """
        pass

    @abstractmethod
    def rnm(self, pool: str, key: str, new_key: str):
        """Rename a key
        """
        pass

    @abstractmethod
    def rm(self, pool: str, key: str):
        """Remove a value from the pool
        """
        pass

    @abstractmethod
    def cleanup(self, pool: str):
        """Cleanup outdated items from the pool
        """
        pass

    @abstractmethod
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
        from pytsite import router as router

        self._server_name = router.server_name()
        self.path = reg.get('cache.file_driver_storage', path.join(reg.get('paths.storage'), 'cache'))

        # Create cache directory
        if not path.exists(self.path):
            makedirs(self.path, 0o755, True)

    def _get_key_path(self, pool: str, key: str) -> str:
        """Get key's file path
        """
        h = util.md5_hex_digest(key)
        return path.join(self.path, self._server_name, pool, h[:2], h[2:4], key.replace(path.sep, '.'))

    def _get_key_dir(self, pool: str, key: str) -> str:
        """Get key's file directory
        """
        return path.dirname(self._get_key_path(pool, key))

    def _store(self, pool: str, key: str, value: Any, ttl: int = None) -> Any:
        """Store an item into the pool
        """
        f_path = self._get_key_path(pool, key)
        d_path = path.dirname(f_path)

        if not path.exists(d_path):
            makedirs(d_path, 0o755)

        with open(f_path, 'wb') as f:
            now = time()
            f.write(pickle_dump({'k': key, 'c': now, 't': ttl, 'e': (now + ttl) if ttl else None, 'v': value}))

        return value

    def _load(self, pool: str, key: str) -> dict:
        """Load an item from the pool
        """
        f_path = self._get_key_path(pool, key)

        try:
            with open(f_path, 'rb') as f:
                return pickle_load(f.read())

        except FileNotFoundError:
            raise _error.KeyNotExist(pool, key)

        except (EOFError, UnpicklingError):
            unlink(f_path)
            raise _error.KeyNotExist(pool, key)

    def _load_check_type(self, pool: str, key: str, expected_type: type) -> dict:
        raw = self._load(pool, key)
        if not isinstance(raw['v'], expected_type):
            raise _error.ValueTypeError(pool, key, raw['v'])

        return raw

    def keys(self, pool: str) -> Generator[str, None, None]:
        """Get all keys of the pool
        """
        for root, dirs, files in walk(path.join(self.path, self._server_name, pool), topdown=False):
            for name in files:
                f_path = path.join(root, name)
                with open(f_path, 'rb') as f:
                    yield pickle_load(f.read())['k']

    def has(self, pool: str, key: str) -> bool:
        """Check whether the pool contains the key
        """
        return path.exists(self._get_key_path(pool, key))

    def type(self, pool: str, key: str) -> Type:
        """Get key's value type
        """
        return type(self._load(pool, key)['v'])

    def put(self, pool: str, key: str, value: Any, ttl: int = None) -> Any:
        """Put an item into the pool
        """
        if isinstance(value, (dict, list)):
            raise _error.ValueTypeError(pool, key, value)

        return self._store(pool, key, value, ttl)

    def get(self, pool: str, key: str) -> Any:
        """Get an item from the pool
        """
        value = self._load(pool, key)['v']
        if isinstance(value, (dict, list)):
            raise _error.ValueTypeError(pool, key, value)

        return value

    def put_hash(self, pool: str, key: str, value: Mapping, ttl: int = None) -> Any:
        """Put a hash item into the pool
        """
        if not isinstance(value, Mapping):
            raise _error.ValueTypeError(pool, key, value)

        return self._store(pool, key, dict(value), ttl)

    def put_hash_item(self, pool: str, key: str, item_key: str, value: Any, ttl: int = None) -> Any:
        """Put a value into a hash
        """
        try:
            raw = self._load_check_type(pool, key, dict)
            val = raw['v']
            val[item_key] = value
            return self._store(pool, key, val, raw['t'])

        except _error.KeyNotExist:
            return self._store(pool, key, {item_key: value}, ttl)

    def get_hash(self, pool: str, key: str, hash_keys: List[str] = None) -> dict:
        """Get hash
        """
        val = self._load_check_type(pool, key, dict)['v']

        return {k: v for k, v in val.items() if k in hash_keys} if hash_keys else val

    def get_hash_item(self, pool: str, key: str, item_key: str, default=None) -> Any:
        """Get a value from a hash
        """
        return self.get_hash(pool, key).get(item_key, default)

    def rm_hash_item(self, pool: str, key: str, item_key: str) -> Any:
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
            raise _error.ValueTypeError(pool, key, value)

        return self._store(pool, key, value, ttl)

    def list_l_push(self, pool: str, key: str, value: Any, ttl: int = None) -> int:
        """Insert the value at the head of the list stored at key
        """
        try:
            raw = self._load_check_type(pool, key, list)
            val = raw['v']
            val.insert(0, value)
            return len(self._store(pool, key, val, raw['t']))
        except _error.KeyNotExist:
            return len(self._store(pool, key, [value], ttl))

    def list_r_push(self, pool: str, key: str, value: Any, ttl: int = None) -> int:
        """Insert the value at the tail of the list stored at key
        """
        try:
            raw = self._load_check_type(pool, key, list)
            val = raw['v']
            val.append(value)
            return len(self._store(pool, key, val, raw['t']))
        except _error.KeyNotExist:
            return len(self._store(pool, key, [value], ttl))

    def list_l_pop(self, pool: str, key: str) -> Any:
        """Remove and return the first element of the list stored at key
        """
        raw = self._load_check_type(pool, key, list)
        val = raw['v']
        r = val.pop(0)
        self._store(pool, key, val, raw['t']) if val else self.rm(pool, key)

        return r

    def list_r_pop(self, pool: str, key: str) -> Any:
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

    def ttl(self, pool: str, key: str) -> Optional[int]:
        """Get remaining time to live of a key
        """
        expires = self._load(pool, key)['e']

        return int(expires - time()) if expires else None

    def rnm(self, pool: str, key: str, new_key: str):
        """Rename a key
        """
        raise NotImplementedError()

    def rm(self, pool: str, key: str):
        """Remove a value from the pool
        """
        try:
            unlink(self._get_key_path(pool, key))
        except FileNotFoundError:
            pass

    def cleanup(self, pool: str):
        """Cleanup outdated items from the cache
        """
        for root, dirs, files in walk(path.join(self.path, self._server_name, pool), topdown=False):
            for name in files:
                f_path = path.join(root, name)
                with open(f_path, 'rb') as f:
                    expires = pickle_load(f.read())['e']

                if expires and expires <= time():
                    try:
                        unlink(f_path)
                    except FileNotFoundError:
                        pass

    def clear(self, pool: str):
        """Clear entire pool
        """
        try:
            rmtree(path.join(self.path, self._server_name, pool))
        except FileNotFoundError:
            pass
