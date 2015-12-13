"""PytSite Wallet Exceptions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AccountExists(Exception):
    pass


class AccountNotExists(Exception):
    pass


class ImproperTransactionState(Exception):
    pass
