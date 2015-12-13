"""Currency Functions
"""
import re as _re
from pytsite import lang as _lang
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


__currencies = []
__main = None


def define(code: str):
    """Define a currency.
    """
    if code in __currencies:
        raise _error.CurrencyAlreadyDefined("Currency '{}' is already defined.".format(code))

    __currencies.append(code)

    if not get_main():
        set_main(code)


def get_all(include_main: bool=True) -> tuple:
    """Get defined currencies.
    """
    if not __currencies:
        raise _error.NoCurrenciesDefined('No currencies was defined.')

    if include_main:
        return tuple(__currencies)
    else:
        return tuple([code for code in __currencies if code != __main])


def get_main() -> str:
    """Get main currency.
    """
    if not __currencies:
        raise _error.NoCurrenciesDefined('No currencies was defined.')

    return __main


def set_main(code: str):
    """Set main currency.
    """
    if code not in __currencies:
        raise _error.CurrencyNotDefined("Currency '{}' is not defined.".format(code))

    global __main
    __main = code


def get(code: str) -> str:
    if code not in __currencies:
        raise _error.CurrencyNotDefined("Currency '{}' is not defined.".format(code))

    return code


def fmt(value: dict, decimal_places: int=2, html=False):
    """Format currency.
    """
    currency = value['currency']
    exp = '%.' + str(decimal_places) + 'f'
    amount = exp % value['amount']
    symbol_before = get_symbol_before(currency)
    symbol_after = get_symbol_after(currency)

    if html:
        integer = _re.sub('^(\d+).+$', '<span class="amount-integer">\\1</span>', amount)
        decimal = ''
        if decimal_places:
            decimal = _re.sub('^\d+\.(\d+)$',
                              '<span class="amount-point">.</span><span class="amount-decimal">\\1</span>', amount)

        amount = '{}{}'.format(integer, decimal)
        if symbol_before:
            symbol_before = '<span class="symbol-before">{}</span>'.format(symbol_before)
        if symbol_after:
            symbol_after = '<span class="symbol-after">{}</span>'.format(symbol_after)

    r = '{} {} {}'.format(symbol_before, amount, symbol_after).strip()

    return r


def get_title(code: str) -> str:
    try:
        return _lang.t('currency_' + get(code) + '_title', exceptions=True)
    except _lang.error.TranslationError:
        return ''


def get_symbol_before(code: str) -> str:
    try:
        return _lang.t('currency_' + get(code) + '_symbol_before', exceptions=True)
    except _lang.error.TranslationError:
        return ''


def get_symbol_after(code: str) -> str:
    try:
        return _lang.t('currency_' + get(code) + '_symbol_after', exceptions=True)
    except _lang.error.TranslationError:
        return ''
