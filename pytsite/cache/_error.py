"""PytSite Cache Errors.
"""

__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Error(Exception):
    pass


class NoDriverRegistered(Error):
    def __str__(self) -> str:
        return 'There is no cache driver registered'


class DriverNotRegistered(Error):
    def __init__(self, name: str):
        self._name = name

    def __str__(self) -> str:
        return "Cache driver '{}' is not registered".format(self._name)


class DriverAlreadyRegistered(Error):
    def __init__(self, name: str):
        self._name = name

    def __str__(self) -> str:
        return "Cache driver '{}' is already registered".format(self._name)


class PoolNotExist(Error):
    def __init__(self, pool_uid: str):
        self._pool_uid = pool_uid

    def __str__(self) -> str:
        return "Pool '{}' is not exists".format(self._pool_uid)


class PoolExists(Error):
    def __init__(self, pool_uid: str):
        self._pool_uid = pool_uid

    def __str__(self) -> str:
        return "Pool '{}' is already exists".format(self._pool_uid)


class KeyNotExist(Error):
    def __init__(self, pool_uid: str, key: str):
        self._pool_uid = pool_uid
        self._key = key

    def __str__(self) -> str:
        return "Pool '{}' does not contain key '{}'".format(self._pool_uid, self._key)


class HashKeyNotExists(Error):
    def __init__(self, pool_uid: str, key: str, hash_key: str):
        self._pool_uid = pool_uid
        self._key = key
        self._hash_key = hash_key

    def __str__(self) -> str:
        return "'{}' pool does not contain key '{}' or key's value is not a hash or it does not contain key '{}'" \
            .format(self._pool_uid, self._key, self._hash_key)


class KeyNeverExpires(Error):
    def __init__(self, pool_uid: str, key: str):
        self._pool_uid = pool_uid
        self._key = key

    def __str__(self) -> str:
        return "Key '{}' in pool '{}' never expires".format(self._key, self._pool_uid)
