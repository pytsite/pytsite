"""PytSite Currency Errors.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class NoCurrenciesDefined(Exception):
    pass


class CurrencyNotDefined(Exception):
    pass


class CurrencyAlreadyDefined(Exception):
    pass
