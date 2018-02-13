"""PytSite Cache Pool
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Mapping as _Mapping, List as _List, Callable as _Callable, Generator as _Generator
from ._driver import Abstract as _Driver


class Pool:
    def __init__(self, uid: str, get_driver: _Callable[[], _Driver]):
        """Init
        """
        self._uid = uid
        self._get_driver = get_driver

    @property
    def uid(self) -> str:
        """Get UID of the pool
        """
        return self._uid

    def keys(self) -> _Generator[str, None, None]:
        """Get all existing keys in current pool
        """
        return self._get_driver().keys(self._uid)

    def has(self, key: str) -> bool:
        """Check whether an item exists in the pool
        """
        return self._get_driver().has(self._uid, key)

    def put(self, key: str, value, ttl: int = None):
        """Put an item into the pool
        """
        return self._get_driver().put(self._uid, key, value, ttl)

    def get(self, key: str):
        """Get an item from the pool
        """
        return self._get_driver().get(self._uid, key)

    def put_hash(self, key: str, value: _Mapping, ttl: int = None):
        """Put a hash item into the pool
        """
        return self._get_driver().put_hash(self._uid, key, value, ttl)

    def put_hash_item(self, key: str, item_key: str, value):
        """Put a value into a hash
        """
        return self._get_driver().put_hash_item(self._uid, key, item_key, value)

    def get_hash(self, key: str, hash_keys: _List[str] = None) -> _Mapping:
        """Get hash
        """
        return self._get_driver().get_hash(self._uid, key, hash_keys)

    def get_hash_item(self, key: str, item_key: str, default=None):
        """Get a value from a hash
        """
        return self._get_driver().get_hash_item(self._uid, key, item_key, default)

    def rm_hash_item(self, key: str, item_key: str):
        """Remove a value from a hash
        """
        return self._get_driver().rm_hash_item(self._uid, key, item_key)

    def l_push(self, key: str, value) -> int:
        """Push a value into beginning of a list
        """
        return self._get_driver().l_push(self._uid, key, value)

    def r_pop(self, key: str):
        """Pop an item from the end of a list
        """
        return self._get_driver().r_pop(self._uid, key)

    def ttl(self, key: str) -> int:
        """Get remaining time to live of a key
        """
        return self._get_driver().ttl(self._uid, key)

    def rnm(self, key: str, new_key: str):
        """Rename a key
        """
        return self._get_driver().rnm(self._uid, key, new_key)

    def rm(self, key: str):
        """Remove a value from the pool
        """
        return self._get_driver().rm(self._uid, key)

    def clear(self):
        """Clear entire pool
        """
        return self._get_driver().clear(self._uid)

    def cleanup(self):
        """Cleanup outdated items from the pool
        """
        return self._get_driver().cleanup(self._uid)
