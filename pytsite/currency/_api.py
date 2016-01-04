"""Currency API Functions
"""
import re as _re
from typing import Tuple as _Tuple
from datetime import datetime as _datetime
from decimal import Decimal as _Decimal
from pytsite import lang as _lang, odm as _odm
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


def get_all(include_main: bool = True) -> _Tuple[str]:
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


def get_rate(source: str, destination: str, date: _datetime=None) -> _Decimal:
    """Get currency exchange rate.
    """
    # Checking currency definitions
    if source not in __currencies:
        raise _error.CurrencyNotDefined("Currency '{}' is not defined.".format(source))
    if destination not in __currencies:
        raise _error.CurrencyNotDefined("Currency '{}' is not defined.".format(destination))

    # Setup ODM finder
    f = _odm.find('currency_rate').where('source', '=', source).where('destination', '=', destination)
    f.sort([('date', _odm.I_DESC)])
    if date:
        f.where('date', '<=', date)

    if f.count():
        # Direct rate found
        return f.first().f_get('rate')
    else:
        # Trying to find reverse rate
        f.remove_where('source').remove_where('destination')
        f.where('source', '=', destination)
        f.where('destination', '=', source)
        if f.count():
            return round(_Decimal(1) / f.first().f_get('rate'), 8)

    # No rate found
    return _Decimal(1)


def exchange(source: str, destination: str, amount: _Decimal, date: _datetime = None) -> _Decimal:
    """Exchange one currency to another.
    """
    if amount is None:
        raise ValueError('Exchange amount must be specified.')

    if isinstance(amount, float):
        amount = str(amount)

    if not isinstance(amount, _Decimal):
        amount = _Decimal(amount)

    return round(amount * get_rate(source, destination, date), 8)


def fmt(currency: str, amount, decimal_places: int = 2, html=False):
    """Format currency string.

    :type amount: float | str | _Decimal
    """
    if currency not in __currencies:
        raise _error.CurrencyNotDefined("Currency '{}' is not defined.".format(currency))

    if isinstance(amount, float):
        amount = str(amount)

    if not isinstance(amount, _Decimal):
        amount = _Decimal(amount)

    amount = str(round(amount, decimal_places))

    symbol = get_symbol(currency)

    if html:
        integer = _re.sub('^(\d+).+$', '<span class="amount-integer">\\1</span>', amount)
        decimal = ''
        if decimal_places:
            decimal = _re.sub('^\d+\.(\d+)$',
                              '<span class="amount-point">.</span><span class="amount-decimal">\\1</span>', amount)

        amount = '{}{}'.format(integer, decimal)
        if symbol:
            symbol = '<span class="symbol">{}</span>'.format(symbol)

    r = '{} {}'.format(amount, symbol).strip()

    return r


def get_title(code: str) -> str:
    """Get currency title.
    """
    if code not in __currencies:
        raise _error.CurrencyNotDefined("Currency '{}' is not defined.".format(code))

    try:
        return _lang.t('pytsite.currency@currency_title_' + code, exceptions=True)
    except _lang.error.TranslationError:
        return _lang.t('currency_title_' + code)


def get_symbol(code: str) -> str:
    """Get currency suffix symbol.
    """
    if code not in __currencies:
        raise _error.CurrencyNotDefined("Currency '{}' is not defined.".format(code))

    try:
        return _lang.t('pytsite.currency@currency_symbol_' + code, exceptions=True)
    except _lang.error.TranslationError:
        return _lang.t('currency_symbol_' + code)
