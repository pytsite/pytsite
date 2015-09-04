"""Currency Functions
"""
import re as _re
from pytsite import lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


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
