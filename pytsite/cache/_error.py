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
    pass


class KeyNeverExpires(Exception):
    pass
