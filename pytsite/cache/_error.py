"""PytSite Cache Errors.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class DriverNotFound(Exception):
    pass


class PoolNotExist(Exception):
    pass


class PoolExists(Exception):
    pass


class KeyNotExist(Exception):
    def __init__(self, pool: str, key: str):
        self._pool = pool
        self._key = key

    def __str__(self) -> str:
        return "Pool '{}' does not contain key '{}'".format(self._pool, self._key)


class HashKeyNotExists(Exception):
    def __init__(self, pool: str, key: str, hash_key: str):
        self._pool = pool
        self._key = key
        self._hash_key = hash_key

    def __str__(self) -> str:
        return "'{}' pool does not contain key '{}' or key's value is not a hash or it does not contain key '{}'" \
            .format(self._pool, self._key, self._hash_key)


class KeyNeverExpires(Exception):
    def __init__(self, pool: str, key: str):
        self._pool = pool
        self._key = key

    def __str__(self) -> str:
        return "Key '{}' in pool '{}' never expires".format(self._key, self._pool)
