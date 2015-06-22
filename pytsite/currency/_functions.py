"""Currency Functions
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
from pytsite.core import lang as _lang

__currencies = []


def define(code: str):
    """Define a currency.
    """
    code = code.upper()
    if code in __currencies:
        raise KeyError("Currency '{}' already defined.")

    __currencies.append(code)


def get_currencies(include_main: bool=True) -> list:
    """Get defined currencies.
    """
    r = []
    for c in __currencies:
        if not include_main and c == get_main_currency():
            continue
        r.append(c)

    return r

def get_main_currency() -> str:
    """Get main currency code.
    """
    if not __currencies:
        raise Exception('No currencies are defined.')

    return __currencies[0]


def get_currency(code: str) -> str:
    code = code.upper()
    if code not in __currencies:
        raise KeyError("Currency '{}' is not defined.")

    return code


def fmt(value: dict, decimal_places: int=2, omit_zeroes: bool=True):
    """Format currency.
    """
    currency = value['currency']
    exp = '%.' + str(decimal_places) + 'f'
    amount = exp % value['amount']

    if omit_zeroes:
        amount = _re.sub('\.0+$', '', amount)

    r = '{} {} {}'.format(get_symbol_before(currency), amount, get_symbol_after(currency)).strip()

    return r

def get_title(code: str) -> str:
    try:
        return _lang.t('currency_' + get_currency(code) + '_title')
    except _lang.error.TranslationError:
        return ''

def get_symbol_before(code: str) -> str:
    try:
        return _lang.t('currency_' + get_currency(code) + '_symbol_before')
    except _lang.error.TranslationError:
        return ''

def get_symbol_after(code: str) -> str:
    try:
        return _lang.t('currency_' + get_currency(code) + '_symbol_after')
    except _lang.error.TranslationError:
        return ''
